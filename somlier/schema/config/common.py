from enum import Enum
from pathlib import PosixPath

from pydantic import BaseModel


def posix_path_to_abs_path(posix_path: PosixPath) -> str:
    return str(posix_path.absolute())


class BaseSchema(BaseModel):
    class Config:
        extra = "allow"
        arbitrary_types_allowed = True
        json_encoders = {PosixPath: posix_path_to_abs_path}


class StrEnum(str, Enum):
    def __str__(self):
        return self.value

    def _serialize(self) -> str:
        return self.value

    @classmethod
    def _deserialize(cls, value: str):
        return cls(value)
