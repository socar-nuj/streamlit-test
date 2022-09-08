from abc import ABC, abstractmethod
from typing import List, Any, Optional

from mlflow.entities import Experiment, Run
from mlflow.entities.model_registry import ModelVersion, RegisteredModel
from mlflow.projects import SubmittedRun

from somlier.application.exceptions import InvalidParameterError, NotFoundError


class MLflowInvalidMetricError(InvalidParameterError):
    pass


class MLflowInvalidRunIDError(InvalidParameterError):
    pass


class MLflowInvalidModelError(InvalidParameterError):
    pass


class MLflowExperimentNotFoundError(NotFoundError):
    pass


class MLflowModelNotFoundError(NotFoundError):
    pass


class MLflowRunNotFoundError(NotFoundError):
    pass


class MLProjectNotFoundError(NotFoundError):
    pass


class MLflowClient(ABC):
    @abstractmethod
    def submit_run(
        self,
        uri: str,
        version: str,
        experiment_name: str,
        use_k8s_job: bool,
        use_gpu: bool,
        entrypoint: str,
        parameters: Optional[dict],
        synchronous: bool = True,
    ) -> SubmittedRun:
        pass

    @abstractmethod
    def get_experiment_by_name(self, experiment_name: str) -> Experiment:
        pass

    @abstractmethod
    def get_registered_model_by_name(self, model_name: str) -> RegisteredModel:
        pass

    @abstractmethod
    def get_run_by_id(self, run_id: str) -> Run:
        pass

    @abstractmethod
    def find_runs_in_experiment_by_metric(self, experiment_id: str, metric: str, ascending: bool) -> List[Run]:
        pass

    @abstractmethod
    def check_if_project_exists(self, uri: str, version: str, entrypoint: str) -> None:
        pass

    @abstractmethod
    def register_model(self, model_name: str, run_id: str) -> ModelVersion:
        pass

    @abstractmethod
    def register_existing_sklearn_model(self, model_name: str, sklearn_model: Any) -> ModelVersion:
        pass

    @abstractmethod
    def register_existing_pytorch_model(self, model_name: str, pytorch_model: Any) -> ModelVersion:
        pass
