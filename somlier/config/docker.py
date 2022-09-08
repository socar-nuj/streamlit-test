from pydantic import Field

from somlier.core.pydantic import DefaultSettings


class DockerCLIConfig(DefaultSettings):
    registry_host: str = Field(default="", env="SOMLIER__DOCKER__REGISTRY_HOST")


class DockerConfig(DefaultSettings):
    cli: DockerCLIConfig = Field(default_factory=DockerCLIConfig)
