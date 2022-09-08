import importlib
import os
import subprocess
import tempfile
from typing import Optional, Any

import joblib
import torch
from git import Repo, GitCommandError
from loguru import logger
from mlflow.entities.model_registry import RegisteredModel, ModelVersion

from somlier.application.ports.clients.mlflow_client import MLflowClient
from somlier.application.use_cases.online.register.exceptions import (
    InvalidTargetDirectoryError,
    SklearnPackageNotFoundError,
    SklearnModuleClassNotFoundError,
    InvalidSklearnModelError,
    LoadPytorchWeightsRuntimeError,
    ArtifactNotFoundInGCSError,
    GitRepositoryNotFoundError,
    PytorchModuleFileNotFoundError,
    PytorchModuleClassNotFoundError,
)
from somlier.application.use_cases.online.register.request import RegisterRequest, RegisterRequestV2
from somlier.application.use_cases.online.register.response import RegisterResponse


class Register:
    def __init__(self, mlflow_client: MLflowClient) -> None:
        self.mlflow_client = mlflow_client

    def execute(self, request: RegisterRequest) -> RegisterResponse:
        run = self.mlflow_client.get_run_by_id(run_id=request.run_id)
        model_version = self.mlflow_client.register_model(model_name=request.model_name, run_id=run.info.run_id)
        return RegisterResponse(message="모델을 등록합니다.", model_version=str(model_version.version))
        # model_version = self._get_model_version_from_run_id(registered_model=registered_model, run_id=request.run_id)
        # if model_version:
        #     return RegisterResponse(model_version=str(model_version), message="이미 등록된 모델입니다. 기존 모델 버전을 반환합니다.")
        #
        # model_version = self.mlflow_client.register_model(mo)
        #
        # try:
        #     for model_version in model.latest_versions:
        #         if model_version.run_id == request.run_id:
        #             return RegisterResponse(
        #                 model_version=str(model_version.version),
        #                 is_newer_version=False,
        #                 message="이미 등록된 모델입니다. 기존 모델 버전을 반환합니다.",
        #             )
        #         else:
        #             model_version = mlflow.register_model(
        #                 model_uri=f"runs:/{request.run_id}/model", name=request.model_name
        #             )
        #             return RegisterResponse(
        #                 model_version=model_version.version, is_newer_version=True, message="모델 버전을 업데이트 합니다."
        #             )
        # except Exception as e:
        #     model_version = mlflow.register_model(model_uri=f"runs:/{request.run_id}/model", name=request.model_name)
        #     return RegisterResponse(
        #         model_version=model_version.version, is_newer_version=True, message="새로운 모델을 등록합니다."
        #     )

        # try:
        #     model = self.mlflow_client.find_registered_model_by_name(model_name=request.model_name)
        #     for model_version in model.latest_versions:
        #         if model_version.run_id == request.run_id:
        #             return RegisterResponse(
        #                 model_version=str(model_version.version),
        #                 is_newer_version=False,
        #                 message="이미 등록된 모델입니다. 기존 모델 버전을 반환합니다.",
        #             )
        #         else:
        #             model_version = mlflow.register_model(
        #                 model_uri=f"runs:/{request.run_id}/model", name=request.model_name
        #             )
        #             return RegisterResponse(
        #                 model_version=model_version.version, is_newer_version=True, message="모델 버전을 업데이트 합니다."
        #             )
        # except Exception as e:
        #     model_version = mlflow.register_model(model_uri=f"runs:/{request.run_id}/model", name=request.model_name)
        #     return RegisterResponse(
        #         model_version=model_version.version, is_newer_version=True, message="새로운 모델을 등록합니다."
        #     )

    @staticmethod
    def _get_model_version_from_run_id(registered_model: RegisteredModel, run_id: str) -> Optional[ModelVersion]:
        for model_version in registered_model.latest_versions:
            if model_version.run_id == run_id:
                return model_version


class RegisterV2:
    def __init__(self, mlflow_client: MLflowClient, default_project_uri: str) -> None:
        self.mlflow_client = mlflow_client
        self.default_project_uri = default_project_uri

    def execute(self, request: RegisterRequestV2) -> RegisterResponse:
        if not request.project_uri:
            request.project_uri = self.default_project_uri

        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                model_version = self._execute_register(directory=tmpdir, **request.dict())
                logger.success(
                    f"모델을 정상적으로 등록했습니다. [{os.environ['MLFLOW_TRACKING_URI']}/#/models/{request.model_name}/versions/{model_version.version}]"
                )
                return RegisterResponse(message="모델을 등록합니다.", model_version=str(model_version.version))
            except Exception as exc:
                logger.error(exc)
                raise

    def _execute_register(
        self,
        model_type: str,
        gcs_uri: str,
        model_name: str,
        project_uri: Optional[str],
        project_name: Optional[str],
        project_ref: Optional[str],
        model_module_path: Optional[str],
        model_class_name: Optional[str],
        directory: str,
    ) -> ModelVersion:

        can_use_directory = os.path.isdir(directory) and os.path.exists(directory)
        if not can_use_directory:
            raise InvalidTargetDirectoryError(title=f"[{directory}] 디렉토리를 이용할 수 없습니다.")

        artifact_path = self._download_from_gcs(gcs_uri, directory)

        # scikit-learn 모델의 경우, 바로 모델을 로드해 mlflow에 register한다.
        if model_type in ("sklearn", "scikit-learn"):
            model_version = self._execute_register_in_sklearn_case(artifact_path, model_name)
        # pytorch 모델의 경우, github 파일을 참조해 모듈 클래스 파일을 로드해 mlflow에 register한다.
        else:
            model = self._clone_from_project_and_import(
                project_uri, project_name, project_ref, model_module_path, model_class_name, directory
            )

            # 모델에 weight을 로드하고, mlflow에 등록한다.
            model_version = self._execute_register_in_pytorch_case(model_name, model, artifact_path)
        return model_version

    def _execute_register_in_sklearn_case(self, artifact_path: str, model_name: str) -> ModelVersion:
        try:
            model = joblib.load(artifact_path)
        except ModuleNotFoundError:
            raise SklearnPackageNotFoundError(title="scikit-learn 라이브러리가 설치되지 않았습니다.")
        except AttributeError as exc:
            raise SklearnModuleClassNotFoundError(
                title="학습된 모델을 로드하는데 필요한 custom 모듈을 import할 수 없습니다.", detail=str(exc.args)
            )
        except KeyError:
            raise InvalidSklearnModelError(title=f"joblib으로 로드할 수 있는 sklearn 모델 파일이 아닙니다.")

        model_version = self.mlflow_client.register_existing_sklearn_model(model_name, model)
        return model_version

    def _execute_register_in_pytorch_case(
        self,
        model_name: str,
        model: Any,
        artifact_path: str,
    ) -> ModelVersion:
        try:
            model.load_state_dict(torch.load(artifact_path, map_location=torch.device("cpu")))
            logger.info("모델에 아티팩트를 정상적으로 로드하였습니다.")
        except RuntimeError as exc:
            raise LoadPytorchWeightsRuntimeError(title="Pytorch 모델에 아티팩트를 정상적으로 로드하지 못했습니다.")

        model_version = self.mlflow_client.register_existing_pytorch_model(model_name, model)
        return model_version

    def _download_from_gcs(self, gcs_uri: str, directory: str) -> str:
        try:
            filename = gcs_uri.split("/")[-1]
            artifact_path = f"{directory}/{filename}"
            subprocess.run(["gsutil", "-m", "cp", gcs_uri, artifact_path], check=True)
            logger.info(f"모델 아티팩트 파일이 다운로드 되었습니다. [{artifact_path}]")
            return artifact_path
        except (FileNotFoundError, subprocess.CalledProcessError):
            raise ArtifactNotFoundInGCSError(title=f"모델 아티팩트 파일이 존재하지 않는 GCS URI입니다. [{gcs_uri}]")

    def _clone_from_project_and_import(
        self,
        project_uri: str,
        project_name: str,
        project_ref: str,
        model_module_path: str,
        model_class_name: str,
        directory: str,
    ) -> Any:

        # project_name, project_ref 기준으로 repository를 clone한다.
        repository_name = project_uri.split("/")[-1].replace(".git", "")
        repository_path = os.path.join(directory, repository_name)
        if not os.path.exists(repository_path):
            os.makedirs(repository_path)

        try:
            repo = Repo.clone_from(url=project_uri, to_path=repository_path, branch=project_ref)
            logger.info(f"[{repository_path}]에 DAG Repo({project_uri})를 클론했습니다.")
        except GitCommandError:
            raise GitRepositoryNotFoundError(
                title=f"존재하지 않는 Repository 또는 ref(branch)입니다. [{project_uri}, {project_ref}]"
            )

        if project_ref in repo.remote("origin").refs:
            repo.remote("origin").pull(project_ref)  # 이미 리모트 저장소에 동일 브랜치가 존재하는 경우 pull합니다.
        logger.info(f"브랜치 [{project_ref}]로 전환하고 최신 상태로 업데이트 하였습니다.")

        # 모듈 파일을 찾아서 import한다.
        full_model_module_path = f"{repository_path}/{project_name}/{model_module_path}"
        try:
            module_spec = importlib.util.spec_from_file_location(
                full_model_module_path.split("/")[-1].replace(".py", ""), full_model_module_path
            )
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
        except (FileNotFoundError, AttributeError):
            raise PytorchModuleFileNotFoundError(
                title="Pytorch 모델의 모듈 경로를 찾을 수 없습니다.", detail=f"{project_name}/{model_module_path}"
            )

        # 입력으로 받은 model class 기준으로 model instance를 만든다.
        # TODO(serena): 모델에 input parameter를 넣어서 인스턴스를 만들어야하는 니즈도 있을 수 있다. kwargs 등으로 입력 받아도 좋을 것 같은데 입력이 너무 길어지는 느낌이 있다.
        try:
            _model = getattr(module, model_class_name)
            model = _model()
        except AttributeError:
            raise PytorchModuleClassNotFoundError(
                title="Pytorch 모델의 클래스를 찾을 수 없습니다.",
                detail=f"{project_name}.{model_module_path.replace('/', '.').replace('.py', '')}.{model_class_name}",
            )

        return model
