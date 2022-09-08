from typing import Optional

import requests
from requests import ConnectTimeout

from somlier.application.ports.clients.k8s_controller_client import (
    DeployResult,
    K8SControllerCleanupError,
    K8SControllerClient,
    K8SControllerDeployError,
)
from somlier.external_interfaces.exceptions import (
    ConnectionTimeoutError,
    HealthcheckError,
)


class K8SControllerRESTClient(K8SControllerClient):
    def __init__(self, host: str, session: Optional[requests.Session] = None) -> None:
        self.host = host
        self.session = session or requests.Session()

    def healthcheck(self) -> None:
        try:
            response = self.session.get(f"{self.host}/healthcheckz")
        except ConnectTimeout as e:
            raise ConnectionTimeoutError(title="somlier k8s controller에 연결할 수 없습니다. VPN이 켜져있나 확인해주세요.", detail=str(e))

        if not response.ok:
            raise HealthcheckError(title="somlier k8s controller 헬스체크에 실패했습니다.")

    def deploy(
        self,
        model_name: str,
        model_version: str,
        service_name: str,
        service_version: str,
        docker_image: str,
        use_gpu: bool = False,
    ) -> DeployResult:
        self.healthcheck()
        response = self.session.post(
            f"{self.host}/api/v1/deploy",
            json={
                "model_name": model_name,
                "model_version": model_version,
                "service_name": service_name,
                "service_version": service_version,
                "docker_image": docker_image,
                "is_gpu": use_gpu,
            },
        )

        if not response.ok:
            raise K8SControllerDeployError(title="배포 중에 오류가 발생했습니다.", detail=response.json().get("message"))

        result = response.json()
        return DeployResult(url=result.get("url"), uid=result.get("uid"))

    def cleanup(self, uid: str) -> None:
        self.healthcheck()
        response = self.session.delete(
            f"{self.host}/api/v1/deploy", json={"istioEnabled": True, "uid": uid}
        )  # TODO(humphrey): istio 여부를 환경 변수로 체크한다

        if not response.ok:
            raise K8SControllerCleanupError(title="클린 업 중에 오류가 발생했습니다.", detail=response.json().get("message"))
