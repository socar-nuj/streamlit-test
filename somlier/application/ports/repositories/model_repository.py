from abc import ABC, abstractmethod
from typing import Optional

from somlier.core.model import Model


class ModelRepository(ABC):
    @abstractmethod
    def find_by_model_name_and_version(self, model_name: str, model_version: str) -> Optional[Model]:
        pass
