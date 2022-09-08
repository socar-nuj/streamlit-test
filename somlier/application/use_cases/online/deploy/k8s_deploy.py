import logging

from bentoml import BentoService
from loguru import logger

from somlier.application.ports.clients.bentoml_client import BentoMLClient
from somlier.application.ports.clients.docker_client import DockerClient
from somlier.application.ports.clients.k8s_controller_client import (
    DeployResult,
    K8SControllerClient,
)
from somlier.application.ports.repositories.model_repository import ModelRepository
from somlier.application.use_cases.online.deploy import (
    Deploy,
    DeployRequest,
    DeployResponse,
)
from somlier.core.model import Model


class K8SDeploy(Deploy):
    def __init__(
        self,
        model_repository: ModelRepository,
        k8s_controller_client: K8SControllerClient,
        docker_client: DockerClient,
        bentoml_client: BentoMLClient,
    ) -> None:
        self.k8s_controller_client = k8s_controller_client
        self.docker_client = docker_client
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
        bento_service, model = self._prepare(model_name=request.model_name, model_version=request.model_version)
        deploy_result = self.__execute(bento_service=bento_service, model=model, request=request)

        return DeployResponse(message=deploy_result.url)

    def __execute(self, bento_service: BentoService, model: Model, request: DeployRequest) -> DeployResult:
        self.logger.info("bento service를 이미지화 합니다.")
        image_name, image_tag = self._bentoml_client.containerize(
            service_name=bento_service.name,
            service_version=bento_service.version,
            image_name=model.name,
            image_tag=model.version,
        )
        self.logger.info(f"만들어진 이미지 이름: {image_name}, 태그: {image_tag}")
        self.logger.info(f"bento service 이미지를 레지스트리에 푸시합니다.")
        docker_image = self.docker_client.push(image_name=image_name, image_tag=image_tag)
        self.logger.info(f"푸시한 이미지: {docker_image}")
        self.logger.info("bento service 이미지를 배포합니다.")
        deploy_result = self.k8s_controller_client.deploy(
            model_name=request.model_name,
            model_version=request.model_version,
            service_name=bento_service.name,
            service_version=bento_service.version,
            docker_image=docker_image,
            use_gpu=request.use_gpu,
        )
        self.logger.info(f"배포된 서버 url: {deploy_result.url}")
        return deploy_result
