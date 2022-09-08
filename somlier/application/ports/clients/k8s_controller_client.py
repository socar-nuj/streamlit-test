from abc import ABC, abstractmethod

from pydantic import BaseModel

from somlier.application.exceptions import ClientError


class DeployResult(BaseModel):
    url: str
    uid: str


class K8SControllerDeployError(ClientError):
    pass


class K8SControllerCleanupError(ClientError):
    pass


class K8SControllerClient(ABC):
    @abstractmethod
    def deploy(
        self,
        model_name: str,
        model_version: str,
        service_name: str,
        service_version: str,
        docker_image: str,
        use_gpu: bool = False,
    ) -> DeployResult:
        pass

    @abstractmethod
    def cleanup(self, uid: str) -> None:
        pass
