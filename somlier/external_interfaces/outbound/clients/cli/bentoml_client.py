from typing import Optional, Tuple

from bentoml import BentoService

from somlier.application.ports.clients.bentoml_client import (
    BentoMLClient,
    BentoMLContainerizeError,
    BentoMLServeError,
)
from somlier.core.bentoml.mlflow.artifact import (
    JsonInputBentoService,
    TensorInputBentoService,
)
from somlier.core.model import Model, ModelInputType
from somlier.external_interfaces.outbound.clients.cli import CLIClient


def create_bento_svc_by_model_input_type(model_input_type: ModelInputType) -> BentoService:
    if model_input_type == ModelInputType.JSON:
        return JsonInputBentoService()

    elif model_input_type == ModelInputType.TENSOR:
        return TensorInputBentoService()

    else:
        raise NotImplementedError()


class BentoMLCLIClient(BentoMLClient):
    def __init__(self, cli_client: CLIClient, default_bentoml_config_path: str) -> None:
        self.cli_client = cli_client
        self.default_bentoml_config_path = default_bentoml_config_path

    def containerize(
        self, service_name: str, service_version: str, image_name: Optional[str], image_tag: Optional[str]
    ) -> Tuple[str, str]:
        error = self.check_image_exists(image_name, image_tag)
        if error:
            return image_name, image_tag

        output, error = self.cli_client.create_subprocess(
            commands=[
                "bentoml",
                "containerize",
                f"{service_name}:{service_version}",
                "-t",
                f"{image_name}:{image_tag}",
            ],
            should_print_output=False,
        )
        if error:
            raise BentoMLContainerizeError(title="bento service를 컨테이너화 하는데 실패했습니다.")
        return image_name, image_tag

    def check_image_exists(self, image_name, image_tag):
        inline_script = (
            f"docker image inspect {image_name}:{image_tag} >/dev/null 2>&1 && >&2 echo yes || echo no".split()
        )
        output, error = self.cli_client.create_subprocess(commands=inline_script, should_print_output=False)
        return error

    def serve(self, service_name: str, service_version: str, config_path: Optional[str] = None) -> None:
        if not config_path:
            config_path = self.default_bentoml_config_path

        output, error = self.cli_client.create_subprocess(
            commands=[
                f"BENTOML_CONFIG={config_path}",
                "bentoml",
                "serve",
                f"{service_name}:{service_version}",
            ]
        )
        if error:
            raise BentoMLServeError(title="bento service를 웹서버로 실행하는데 실패했습니다.", detail=error)

    def create_bento_service(self, model_input_type: ModelInputType) -> BentoService:
        return create_bento_svc_by_model_input_type(model_input_type=model_input_type)

    def save_to_yatai(self, model: Model, bento_svc: BentoService) -> str:
        if not isinstance(bento_svc, BentoService):
            raise BentoMLServeError(title="올바른 BentoService가 아닙니다")

        bento_svc.pack("model", model)
        saved_path: str = bento_svc.save()
        return saved_path
