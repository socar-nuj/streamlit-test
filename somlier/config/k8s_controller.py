from pydantic import BaseSettings, Field


class K8SControllerRESTConfig(BaseSettings):
    host: str = Field(
        default="", env="SOMLIER__K8S_CONTROLLER_REST_HOST", description="K8S Controller REST API Host 이름"
    )


class K8SControllerConfig(BaseSettings):
    rest: K8SControllerRESTConfig = Field(default_factory=K8SControllerRESTConfig)
