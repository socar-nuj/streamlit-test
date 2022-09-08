from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class CleanupRequest(BaseModel):
    model_name: Optional[str]
    model_version: Optional[str]
    uid: Optional[str]


class CleanupStatus(str, Enum):
    SUCCESS = "success"
    FAILURE = "failure"


class CleanupResponse(BaseModel):
    message: str
    status: CleanupStatus


class Cleanup(ABC):
    @abstractmethod
    def execute(self, request: CleanupRequest) -> CleanupResponse:
        ...
