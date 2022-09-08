from somlier.application.ports.clients.docker_client import (
    DockerCLIClientError,
    DockerClient,
)
from somlier.external_interfaces.outbound.clients.cli import CLIClient


class DockerCLIClient(DockerClient):
    def __init__(self, registry_host: str, cli_client: CLIClient) -> None:
        self._registry_host = registry_host
        self.cli_client = cli_client

    def push(self, image_name: str, image_tag: str) -> str:
        docker_image_concatenated = f"{image_name}:{image_tag}"
        full_image_name = f"{self.registry_host}/{docker_image_concatenated}"
        exists_in_registry = self.check_if_exists_in_registry(full_image_name)
        if exists_in_registry:
            return full_image_name

        output, err = self.cli_client.create_subprocess(
            commands=["docker", "tag", docker_image_concatenated, full_image_name]
        )
        if err:
            raise DockerCLIClientError("Docker 이미지를 tag하는 과정이 실패했습니다", detail=err)
        output, err = self.cli_client.create_subprocess(commands=["docker", "push", full_image_name])
        if err:
            raise DockerCLIClientError("Docker 이미지를 push하는 과정이 실패했습니다", detail=err)
        return full_image_name

    def check_if_exists_in_registry(self, full_image_name):
        script_ = f"docker manifest inspect {full_image_name} > /dev/null ; echo $?".split()
        output, err = self.cli_client.create_subprocess(commands=script_, should_print_output=False)
        return not err

    @property
    def registry_host(self) -> str:
        return self._registry_host
