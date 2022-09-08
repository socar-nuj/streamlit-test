from enum import Enum

from pydantic import Field

from somlier.config.airflow import AirflowConfig
from somlier.config.bentoml import BentoMLConfig
from somlier.config.docker import DockerConfig
from somlier.config.k8s_controller import K8SControllerConfig
from somlier.config.mlflow import MLflowConfig
from somlier.core.pydantic import DefaultSettings

from .configure import Struct, configure


class AppConfigEnv(str, Enum):
    DEV = "dev"
    PROD = "prod"
    TEST = "test"


class AppConfig(DefaultSettings):
    env: AppConfigEnv = Field(default=AppConfigEnv.DEV)
    docker: DockerConfig = Field(default_factory=DockerConfig)
    mlflow: MLflowConfig = Field(default_factory=MLflowConfig)
    airflow: AirflowConfig = Field(default_factory=AirflowConfig)
    bentoml: BentoMLConfig = Field(default_factory=BentoMLConfig)
    k8s_controller: K8SControllerConfig = Field(default_factory=K8SControllerConfig)
