from abc import ABC, abstractmethod
from typing import List


class DAGBuilderClient(ABC):
    @property
    @abstractmethod
    def can_use(self) -> bool:
        pass

    @abstractmethod
    def generate(self, args: List[str]) -> str:
        pass
