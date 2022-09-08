import logging

from loguru import logger

from somlier.application.ports.clients.bentoml_client import BentoMLClient
from somlier.application.ports.repositories.model_repository import ModelRepository
from somlier.application.use_cases.online.deploy import (
    Deploy,
    DeployRequest,
    DeployResponse,
)


class LocalDeploy(Deploy):
    def __init__(
        self,
        model_repository: ModelRepository,
        bentoml_client: BentoMLClient,
    ) -> None:
        self._model_repository = model_repository
        self._bentoml_client = bentoml_client
        self._logger = logger

    @property
    def model_repository(self) -> ModelRepository:
        return self._model_repository

    @property
    def bentoml_client(self) -> BentoMLClient:
        return self._bentoml_client

    @property
    def logger(self) -> logging.Logger:
        return self._logger

    def execute(self, request: DeployRequest) -> DeployResponse:
        """모델 저장소로 부터 아티펙트를 로컬에 다운로드하고, 웹서버 프로세스를 띄웁니다."""
        bento_service, model = self._prepare(model_name=request.model_name, model_version=request.model_version)

        self.logger.info("bento service를 실행합니다.")
        self.bentoml_client.serve(service_name=bento_service.name, service_version=bento_service.version)

        return DeployResponse(message="bento service 실행을 완료했습니다.")
