from pydantic import Field

from somlier.core.pydantic import DefaultSettings


class BentoMLConfig(DefaultSettings):
    config_path: str = Field(default="", env="SOMLIER__BENTOML__CONFIG_PATH")
