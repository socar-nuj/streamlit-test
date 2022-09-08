from abc import ABC, abstractmethod
from typing import Any, Dict, List

from somlier.core.exceptions import Error


class AirflowClientError(Error):
    pass


class AirflowClient(ABC):
    @abstractmethod
    def find_dag(self, dag_id: str) -> str:
        pass

    @abstractmethod
    def list_dags(self) -> List[Dict[str, Any]]:
        pass
