from enum import Enum
from typing import Any, Dict, Optional

from google.api_core.exceptions import NotFound
from mlflow.pyfunc import PyFuncModel, load_model
from mlflow.types import TensorSpec
from pydantic import BaseModel, Field

from somlier.core.exceptions import Error


class ModelInputType(str, Enum):
    TENSOR = "TENSOR"
    JSON = "JSON"


class ModelNotFoundInRegistry(Error):
    pass


class Model(BaseModel):
    model_uri: Optional[str] = None
    name: str
    version: str
    tags: Dict[str, Any] = Field(default_factory=dict)

    @property
    def py_func_model(self) -> PyFuncModel:
        try:
            return load_model(model_uri=self.model_uri)
        except NotFound:
            raise ModelNotFoundInRegistry(
                title="GCS로 부터 모델을 가져올 수 없습니다",
                detail=f"Model Name: {self.name}, Model Version: {self.version}, GCS URI: {self.model_uri}",
            )

    @property
    def input_type(self) -> ModelInputType:
        if isinstance(self.py_func_model.metadata.signature.inputs.inputs[0], TensorSpec):
            return ModelInputType.TENSOR
        else:
            return ModelInputType.JSON

    @property
    def model_filename(self) -> str:
        return self.py_func_model.metadata.flavors.get("python_function", {}).get("data", None)

    class Config:
        arbitrary_types_allowed = True
