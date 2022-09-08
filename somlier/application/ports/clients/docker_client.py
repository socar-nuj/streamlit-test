from abc import ABC, abstractmethod

from somlier.core.exceptions import Error


class DockerCLIClientError(Error):
    pass


class DockerClient(ABC):
    @abstractmethod
    def push(self, image_name: str, image_tag: str) -> str:
        pass

    @property
    @abstractmethod
    def registry_host(self) -> str:
        pass
