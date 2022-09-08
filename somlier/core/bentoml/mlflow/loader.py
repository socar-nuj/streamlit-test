from abc import ABC, abstractmethod

from bentoml.frameworks import lightgbm, pytorch, sklearn
from bentoml.service import BentoServiceArtifact


class MLflowArtifactLoader(ABC):
    @abstractmethod
    def create(self) -> BentoServiceArtifact:
        pass

    def load(self, path) -> ...:
        loader = self.create()
        return loader.load(path)


class MLflowArtifactSklearnLoader(MLflowArtifactLoader):
    def create(self) -> BentoServiceArtifact:
        return sklearn.SklearnModelArtifact("model")


class MLflowArtifactLightgbmLoader(MLflowArtifactLoader):
    def create(self) -> BentoServiceArtifact:
        return lightgbm.LightGBMModelArtifact(
            "model", model_extension=".lgb"
        )  # TODO(humphrey): lightgbm artifact를 model_extension override 가능하게 래핑한다


class MLflowArtifactPytorchLoader(MLflowArtifactLoader):
    def __init__(self, file_extension: str = ".pt") -> None:
        self._file_extension = file_extension

    def create(self) -> BentoServiceArtifact:
        return pytorch.PytorchModelArtifact("model", file_extension=self._file_extension)
