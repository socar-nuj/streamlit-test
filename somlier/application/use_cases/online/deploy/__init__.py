import logging
from abc import ABC, abstractmethod
from typing import NewType, Tuple

from bentoml import BentoService
from pydantic import BaseModel

from somlier.application.exceptions import NotFoundError
from somlier.application.ports.clients.bentoml_client import BentoMLClient
from somlier.application.ports.repositories.model_repository import ModelRepository
from somlier.core.model import Model

BentoServiceLocalPath = NewType("BentoServiceLocalPath", str)
BentoServiceName = NewType("BentoServiceName", str)
BentoServiceVersion = NewType("BentoServiceVersion", str)


class DeployRequest(BaseModel):
    model_name: str
    model_version: str
    use_k8s: bool = True  # TODO(humphrey): docker image별, 환경별 테스트 가능하게 하기
    use_gpu: bool = False
    istio_enabled: bool = False


class DeployResponse(BaseModel):
    message: str


class ModelNotFoundError(NotFoundError):
    pass


class Deploy(ABC):
    @property
    @abstractmethod
    def model_repository(self) -> ModelRepository:
        pass

    @property
    @abstractmethod
    def bentoml_client(self) -> BentoMLClient:
        pass

    @property
    @abstractmethod
    def logger(self) -> logging.Logger:
        pass

    @abstractmethod
    def execute(self, request: DeployRequest) -> DeployResponse:
        pass

    # TODO: use external cache with redis
    def _prepare(self, model_name: str, model_version: str) -> Tuple[BentoService, Model]:
        model = self.model_repository.find_by_model_name_and_version(
            model_name=model_name, model_version=model_version
        )
        if not model:
            raise ModelNotFoundError(title="요청에 해당하는 모델을 찾을 수 없습니다.")
        self.logger.info("bento service를 만듭니다.")
        bento_service = self.bentoml_client.create_bento_service(model_input_type=model.input_type)
        bento_service_local_path = self.bentoml_client.save_to_yatai(model=model, bento_svc=bento_service)
        self.logger.info(
            f"bento service 경로: {bento_service_local_path}, 이름: {bento_service.name}, 버전: {bento_service.version}, "
        )
        return bento_service, model
