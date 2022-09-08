import os
from typing import Optional, Tuple

from bentoml import BentoService, api, artifacts, env
from bentoml.adapters import JsonInput, TfTensorInput
from bentoml.service import BentoServiceArtifact
from google.cloud import storage

from somlier.core.bentoml.exceptions import (
    ArtifactFileNotFoundError,
    ArtifactUnknownExtensionError,
)
from somlier.core.bentoml.mlflow.loader import (
    MLflowArtifactLightgbmLoader,
    MLflowArtifactLoader,
    MLflowArtifactPytorchLoader,
    MLflowArtifactSklearnLoader,
)
from somlier.core.model import Model

_SUPPORTED_ARTIFACT_EXTENSION = {".pkl", ".lgb", ".pth", ".pt"}


class MLflowGCSArtifact(BentoServiceArtifact):
    def __init__(self, name: str) -> None:
        super().__init__(name=name)
        self._model: Optional[Model] = None

    @property
    def storage_client(self) -> storage.Client:
        return storage.Client()

    @property
    def gcs_uri(self) -> Optional[str]:
        return self._model.model_uri or None

    @property
    def gcs_bucket_and_key(self) -> Tuple[str, str]:
        def _remove_prefix(text: str, prefix: str) -> str:
            return text[text.startswith(prefix) and len(prefix) :]

        split_paths = _remove_prefix(self.gcs_uri, "gs://").split("/")

        return split_paths[0], "/".join(split_paths[1:])

    def _file_path(self, base_path: str, filepath: Optional[str] = None) -> str:
        if filepath:
            return os.path.join(base_path, filepath)

        return os.path.join(base_path, self._model.model_filename)

    def pack(self, model: Model, metadata: Optional[dict] = None) -> "MLflowGCSArtifact":
        self._model = model
        super().pack(model=model, metadata=metadata)
        return self

    def get(self) -> Optional[Model]:
        return self._model

    def save(self, dst: str) -> None:
        bucker_name, key = self.gcs_bucket_and_key
        bucket = self.storage_client.get_bucket(bucker_name)
        blobs = list(bucket.list_blobs(prefix=key))

        if not os.path.exists(dst):
            os.makedirs(dst)

        for blob in blobs:
            if not blob.name:
                continue

            blob_filename = blob.name.split("/")[-1]
            blob.download_to_filename(f"{dst}/{blob_filename}")

    def load(self, path) -> "MLflowGCSArtifact":
        loader = self._create_loader(path=path)
        model = loader.load(path=path)
        return self.pack(model=model)

    def _create_loader(self, path) -> MLflowArtifactLoader:
        file_list = os.listdir(path=path)
        target_file = None
        for file in file_list:
            if file.startswith("model") and any([file.endswith(_format) for _format in _SUPPORTED_ARTIFACT_EXTENSION]):
                target_file = file

        if not target_file:
            raise ArtifactFileNotFoundError(title="아티펙트를 찾을 수 없습니다", detail=f"target_file: {target_file}")

        if target_file.endswith(".lgb"):
            return MLflowArtifactLightgbmLoader()

        if target_file.endswith(".pkl"):
            return MLflowArtifactSklearnLoader()

        if target_file.endswith(".pth"):
            return MLflowArtifactPytorchLoader(file_extension=".pth")

        if target_file.endswith(".pt"):
            return MLflowArtifactPytorchLoader(file_extension=".pt")

        raise ArtifactUnknownExtensionError(title="알수 없는 확장자 입니다")


@env(infer_pip_packages=True)
@artifacts([MLflowGCSArtifact("model")])
class JsonInputBentoService(BentoService):
    @api(input=JsonInput(), batch=False)
    def predict(self, input_data):
        return self.artifacts.model.get().predict(input_data)


@env(infer_pip_packages=True, pip_packages=["torch==1.8.0", "tensorflow"])
@artifacts([MLflowGCSArtifact("model")])
class TensorInputBentoService(BentoService):
    @api(input=TfTensorInput(), batch=True)
    def predict(self, input_data):
        return self.artifacts.model.get().predict(input_data)
