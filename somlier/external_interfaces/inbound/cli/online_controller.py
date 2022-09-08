from typing import Optional, Dict, Any

from somlier.application.use_cases.online.cleanup import CleanupRequest
from somlier.application.use_cases.online.deploy import DeployRequest
from somlier.application.use_cases.online.register.request import RegisterRequest, RegisterRequestV2
from somlier.application.use_cases.online.search import SearchRequest
from somlier.application.use_cases.online.train.request import TrainRequest
from somlier.external_interfaces.container import OnlineContainer


class OnlineController:
    def __init__(self, container: OnlineContainer) -> None:
        self.container = container

    def train(
        self,
        project_name: str,
        project_ref: str,
        github_uri: Optional[str] = None,
        use_k8s_job: bool = False,
        use_gpu: bool = False,
        **params: Optional[Dict[str, Any]],
    ) -> None:
        """MLflow Project를 실행합니다."""

        if not github_uri:
            github_uri = self.container.config.mlflow.default_project_uri()

        request = TrainRequest(
            project_name=project_name,
            project_uri=github_uri,
            project_ref=project_ref,
            use_k8s_job=use_k8s_job,
            use_gpu=use_gpu,
            params=params,
        )

        use_case = self.container.train()
        responses = use_case.execute(request)
        print(f"{len(responses)} experiments submitted.")

    def search(self, project_name: str, metric_by: str, ascending: bool = False) -> None:
        """MLflow Project에서 metric 값이 가장 낮거나 높은 실행을 검색합니다."""

        request = SearchRequest(project_name=project_name, metric_by=metric_by, ascending=ascending)
        use_case = self.container.search()
        response = use_case.execute(request)

        print(f"run id: {response.run_id}")
        print(f"standard metric value: {response.metric_value}")

    def register(self, run_id: str, model_name: str) -> None:
        """MLflow 실행의 모델을 레지스트리에 등록합니다."""

        request = RegisterRequest(run_id=run_id, model_name=model_name)
        use_case = self.container.register()
        response = use_case.execute(request)

        print(f"model version: {response.model_version}")
        print(response.message)

    def register_v2(
        self,
        model_type: str,
        gcs_uri: str,
        model_name: str,
        github_uri: Optional[str] = None,
        project_name: Optional[str] = None,
        project_ref: Optional[str] = "main",
        model_module_path: Optional[str] = None,
        model_class_name: Optional[str] = None,
    ) -> None:
        """기존에 학습이 완료된 머신러닝 (sklearn, pytorch) 모델을 레지스트리에 등록합니다."""

        request = RegisterRequestV2(
            model_type=model_type,
            gcs_uri=gcs_uri,
            model_name=model_name,
            project_uri=github_uri,
            project_name=project_name,
            project_ref=project_ref,
            model_module_path=model_module_path,
            model_class_name=model_class_name,
        )
        use_case = self.container.register_v2()
        response = use_case.execute(request)

    def deploy(
        self,
        model_name: str,
        model_version: str,
        use_k8s: bool = False,
        istio_enabled: bool = False,
        use_gpu: bool = False,
    ) -> None:
        """MLflow Registry에 등록된 모델을 배포합니다."""

        request = DeployRequest(
            model_name=model_name,
            model_version=model_version,
            use_k8s=use_k8s,
            istio_enabled=istio_enabled,
            use_gpu=use_gpu,
        )
        if use_k8s:
            use_case = self.container.k8s_deploy()
        else:
            use_case = self.container.local_deploy()
        response = use_case.execute(request)

        print(response.message)

    def cleanup(self, uid: str) -> None:  # TODO(humphrey): model_name, model_version으로도 cleanup할 수 있게한다
        """배포된 모델을 제거합니다 (K8S only)"""

        request = CleanupRequest(uid=uid)
        use_case = self.container.cleanup()
        response = use_case.execute(request)

        print(response.message)

    def server(self) -> None:
        """백엔드 서버를 실행합니다."""
        from somlier.external_interfaces.inbound.web import run_server

        run_server()
