from loguru import logger

from somlier.application.ports.clients.k8s_controller_client import K8SControllerClient
from somlier.application.use_cases.online.cleanup import (
    Cleanup,
    CleanupRequest,
    CleanupResponse,
    CleanupStatus,
)


class K8SCleanup(Cleanup):
    def __init__(self, k8s_controller_client: K8SControllerClient) -> None:
        self.k8s_controller_client = k8s_controller_client
        self._logger = logger

    def execute(self, request: CleanupRequest) -> CleanupResponse:
        self.k8s_controller_client.cleanup(request.uid)
        return CleanupResponse(status=CleanupStatus.SUCCESS, message="Deploy된 모델이 제거됐습니다.")
