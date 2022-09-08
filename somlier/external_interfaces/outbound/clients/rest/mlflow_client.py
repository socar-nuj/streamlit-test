import os
import shutil
from typing import List, Optional, Any

import mlflow
import requests
from mlflow.entities import Experiment, Run
from mlflow.entities.model_registry import ModelVersion, RegisteredModel
from mlflow.exceptions import MlflowException, RestException
from mlflow.projects import SubmittedRun
from mlflow.tracking import MlflowClient
from pydantic import FilePath, HttpUrl
from requests.exceptions import ConnectTimeout

from somlier.application.ports.clients.mlflow_client import (
    MLflowClient,
    MLflowExperimentNotFoundError,
    MLflowInvalidMetricError,
    MLflowInvalidRunIDError,
    MLflowInvalidModelError,
    MLflowModelNotFoundError,
    MLflowRunNotFoundError,
    MLProjectNotFoundError,
)
from somlier.external_interfaces.exceptions import (
    ConnectionTimeoutError,
    HealthcheckError,
)


class MLflowRESTClient(MLflowClient):
    def __init__(
        self,
        mlflow_tracking_uri: HttpUrl,
        kube_context: str,
        kube_config_path: FilePath,
        kube_repository_uri: HttpUrl,
        kube_job_template_path: FilePath,
        kube_job_with_gpu_template_path: FilePath,
        session: Optional[requests.Session] = None,
    ) -> None:
        os.environ["MLFLOW_TRACKING_URI"] = mlflow_tracking_uri
        self.mlflow_tracking_uri = mlflow_tracking_uri
        self.kube_context = kube_context
        self.kube_config_path = kube_config_path
        self.kube_repository_uri = kube_repository_uri
        self.kube_job_template_path = kube_job_template_path
        self.kube_job_with_gpu_template_path = kube_job_with_gpu_template_path
        self._mlflow_client = MlflowClient(tracking_uri=mlflow_tracking_uri)
        self.session = session or requests.Session()

    def submit_run(
        self,
        uri: str,
        version: str,
        experiment_name: str,
        use_k8s_job: bool,
        use_gpu: bool,
        entrypoint: str = "main",
        parameters: dict = None,
        synchronous: bool = True,
    ) -> SubmittedRun:
        self.healthcheck()
        if use_k8s_job:
            backend = "kubernetes"
            backend_config = {
                "kube-context": self.kube_context,
                "repository-uri": self.kube_repository_uri,
            }
            if not use_gpu:
                backend_config["kube-job-template-path"] = self.kube_job_template_path
            else:
                backend_config["kube-job-template-path"] = self.kube_job_with_gpu_template_path
        else:
            backend = "local"
            backend_config = {}

        if parameters is None:
            parameters = {}

        # TODO(serena): synchronous=False로 뒀을때 docker build, kubernetes 관련된 print문이 계속 출력되는 이슈 (내장 함수)
        try:
            submitted_run = mlflow.run(
                uri=uri,
                entry_point=entrypoint,
                version=version,
                experiment_name=experiment_name,
                backend=backend,
                backend_config=backend_config,
                parameters=parameters,
                synchronous=synchronous,  # 실험 정보를 client를 통해 요청만 하고 바로 돌아오게 수정한다.
            )
            return submitted_run
        except MlflowException as e:
            raise

    def get_experiment_by_name(self, experiment_name: str) -> Experiment:
        self.healthcheck()
        try:
            return self._mlflow_client.get_experiment_by_name(name=experiment_name)
        except RestException as e:
            if e.error_code == "RESOURCE_DOES_NOT_EXIST":
                raise MLflowExperimentNotFoundError(title="해당하는 experiment가 존재하지 않습니다.", detail=str(e))

    def get_registered_model_by_name(self, model_name: str) -> RegisteredModel:
        self.healthcheck()
        try:
            return self._mlflow_client.get_registered_model(name=model_name)
        except RestException as e:
            if e.error_code == "RESOURCE_DOES_NOT_EXIST":
                raise MLflowModelNotFoundError(title="해당하는 model이 존재하지 않습니다.", detail=str(e))

    def get_run_by_id(self, run_id: str) -> Run:
        self.healthcheck()
        try:
            return self._mlflow_client.get_run(run_id=run_id)
        except RestException as e:
            if e.error_code == "RESOURCE_DOES_NOT_EXIST":
                raise MLflowRunNotFoundError(title="해당하는 run이 존재하지 않습니다.", detail=str(e))
        except MlflowException as exc:
            raise MLflowInvalidRunIDError(title="run_id 값이 유효하지 않습니다", detail=exc.message)

    def find_runs_in_experiment_by_metric(self, experiment_id: str, metric: str, ascending: bool) -> List[Run]:
        self.healthcheck()
        try:
            if ascending:
                sort_string = "ASC"
            else:
                sort_string = "DESC"
            return mlflow.search_runs(
                experiment_ids=[experiment_id],
                order_by=[
                    f"metrics.{metric} {sort_string}",
                ],
                max_results=1,
                output_format="list",
            )
        except RestException as e:
            if e.error_code == "INVALID_PARAMETER_VALUE":
                raise MLflowInvalidMetricError(title="metric 값이 유효하지 않습니다.", detail=str(e))

    def check_if_project_exists(self, uri: str, version: str, entrypoint: str) -> None:
        self.healthcheck()
        work_dir = None
        try:
            work_dir = mlflow.projects.fetch_and_validate_project(
                uri=uri, version=version, entry_point=entrypoint, parameters=None
            )
        except MlflowException as e:
            err_msg = str(e)
            if "Could not find subdirectory" in err_msg:
                raise MLProjectNotFoundError(title="해당하는 프로젝트가 존재하지 않습니다.", detail=err_msg)
            elif "Unable to checkout version" in err_msg:
                raise MLProjectNotFoundError(title="해당하는 프로젝트의 버전이 존재하지 않습니다.", detail=err_msg)
            else:
                raise e
        finally:
            if work_dir:
                shutil.rmtree(work_dir)

    def register_model(self, model_name: str, run_id: str) -> ModelVersion:
        self.healthcheck()
        try:
            model_version = mlflow.register_model(model_uri=f"runs:/{run_id}/model", name=model_name)
        except MlflowException as exc:
            raise MLflowInvalidRunIDError(title="run_id 값이 유효하지 않습니다", detail=exc.message)
        return model_version

    def register_existing_sklearn_model(self, model_name: str, sklearn_model: Any) -> ModelVersion:
        self.healthcheck()
        try:
            model_info = mlflow.sklearn.log_model(sklearn_model, model_name)
        except MlflowException as exc:
            raise MLflowInvalidModelError(title="mlflow.sklearn.log_model의 입력으로 유효하지 않은 모델입니다.", detail=exc.message)
        return self.register_model(model_name, model_info.run_id)

    def register_existing_pytorch_model(self, model_name: str, pytorch_model: Any) -> ModelVersion:
        self.healthcheck()
        try:
            model_info = mlflow.pytorch.log_model(pytorch_model, model_name)
        except MlflowException as exc:
            raise MLflowInvalidModelError(title="mlflow.pytorch.log_model의 입력으로 유효하지 않은 모델입니다.", detail=exc.message)
        return self.register_model(model_name, model_info.run_id)

    def healthcheck(self) -> None:
        try:
            response = self.session.get(f"{self.mlflow_tracking_uri}/health", timeout=5)
        except ConnectTimeout as e:
            raise ConnectionTimeoutError(title="mlflow에 연결할 수 없습니다. VPN이 켜져있나 확인해주세요.", detail=str(e))

        if not response.ok:
            raise HealthcheckError(title="mlflow 헬스체크에 실패했습니다.")
