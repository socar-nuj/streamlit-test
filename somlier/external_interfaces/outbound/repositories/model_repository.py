from typing import Optional

from mlflow.entities.model_registry import ModelVersion

from somlier.application.ports.clients.mlflow_client import (
    MLflowClient,
    MLflowModelNotFoundError,
)
from somlier.application.ports.repositories.model_repository import ModelRepository
from somlier.core.model import Model


class MLflowModelRepository(ModelRepository):
    def __init__(self, mlflow_client: MLflowClient) -> None:
        self.mlflow_client = mlflow_client

    def find_by_model_name_and_version(self, model_name: str, model_version: str) -> Optional[Model]:
        try:
            registered_model = self.mlflow_client.get_registered_model_by_name(model_name=model_name)
        except MLflowModelNotFoundError:
            return

        model_version: ModelVersion = next(
            (mv for mv in registered_model.latest_versions if mv.version == model_version), None
        )
        if not model_version:
            return

        return Model(
            name=model_version.name,
            version=model_version.version,
            tags=model_version.tags,
            model_uri=model_version.source,
        )
