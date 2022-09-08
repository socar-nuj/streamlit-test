from enum import Enum

from pydantic import Field

from somlier.schema.config.common import BaseSchema


class SomlierLoggingFormat(str, Enum):
    TEXT = "text"
    JSON = "json"


class SomlierLoggingConfig(BaseSchema):
    format: SomlierLoggingFormat = Field(default=SomlierLoggingFormat.JSON)


class SomlierGlobalConfig(BaseSchema):
    env: str = Field(default="dev", env="ENV")
    logging: SomlierLoggingConfig = Field(default_factory=SomlierLoggingConfig)
