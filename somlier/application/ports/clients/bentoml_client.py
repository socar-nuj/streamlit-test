from abc import ABC, abstractmethod
from typing import Optional, Tuple

from bentoml import BentoService

from somlier.application.exceptions import ApplicationError
from somlier.core.model import Model, ModelInputType


class BentoMLContainerizeError(ApplicationError):
    pass


class BentoMLServeError(ApplicationError):
    pass


class BentoMLClient(ABC):
    @abstractmethod
    def containerize(
        self, service_name: str, service_version: str, image_name: Optional[str], image_tag: Optional[str]
    ) -> Tuple[str, str]:
        pass

    @abstractmethod
    def serve(self, service_name: str, service_version: str, config_path: Optional[str] = None) -> None:
        pass

    @abstractmethod
    def create_bento_service(self, model_input_type: ModelInputType) -> BentoService:
        pass

    @abstractmethod
    def save_to_yatai(self, model: Model, bento_svc: BentoService) -> str:
        pass
