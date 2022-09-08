from typing import List, Optional, Union

from pydantic import Field, validator

from somlier.config.configure import Struct
from somlier.schema.config.assets import SomlierModelAsset
from somlier.schema.config.common import BaseSchema


class SomlierModel(BaseSchema):
    name: str
    version: str
    tags: List[str]
    assets: List[SomlierModelAsset] = Field(default_factory=list)
    config: Optional[Union[Struct, dict]] = Field(default_factory=dict)

    @validator("version")
    def version_must_start_with_v(cls, version: str):
        if not version.startswith("v"):
            raise ValueError("모델에 v prefix를 붙혀주세요")
        return version
