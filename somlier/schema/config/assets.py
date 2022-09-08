import os
from typing import Dict, Generic, List, TypeVar
from urllib.parse import urlparse

from google.cloud import storage
from pydantic.dataclasses import dataclass

from somlier.schema.config.common import BaseSchema, StrEnum


class SomlierModelAssetProvider(StrEnum):
    GCS = "gcs"
    HTTP = "http"


P = TypeVar("P", bound=SomlierModelAssetProvider)


@dataclass(frozen=True)
class SomlierGCSAsset:
    uri: str
    target_path: str

    def __post_init__(self):
        if not self.uri.startswith("gs://"):
            raise ValueError("잘못된 gcs uri입니다. e.g., gs://socar-data-temp/asset.pth")

    @property
    def parsed_url_object(self):
        return urlparse(self.uri)

    @property
    def bucket_name(self) -> str:
        return self.parsed_url_object.netloc

    @property
    def key_name(self) -> str:
        return self.parsed_url_object.path.lstrip("/")


class SomlierModelAssetFile(BaseSchema):
    remote_uri: str
    local_path: str


class SomlierModelAssetHandlerContext(BaseSchema):
    base_dir: str
    files: Dict[str, SomlierModelAssetFile]


C = TypeVar("C", bound=SomlierModelAssetHandlerContext)


class SomlierModelAssetHandler(BaseSchema, Generic[P, C]):
    provider = ""

    def handle(self, ctx: C) -> None:
        pass


class CredentialEnvVarNotFound(Exception):
    pass


class SomlierModelGCSAssetHandler(
    SomlierModelAssetHandler[SomlierModelAssetProvider.GCS, SomlierModelAssetHandlerContext]
):
    provider = SomlierModelAssetProvider.GCS.value

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.client = storage.Client()
        except OSError:
            raise CredentialEnvVarNotFound(
                "환경 변수로 부터 올바른 GOOGLE_APPLICATION_CREDENTIALS 값을 가져올 수 없습니다. 사용할 service account json 경로를 다시 입력해주세요"
            )

    def handle(self, ctx: SomlierModelAssetHandlerContext) -> List[str]:
        super().handle(ctx=ctx)
        gcs_assets = [SomlierGCSAsset(uri=file.remote_uri, target_path=file.local_path) for file in ctx.files.values()]
        if not os.path.exists(ctx.base_dir):
            os.mkdir(ctx.base_dir)
        handled_files = []
        for gcs_asset in gcs_assets:
            bucket = self.client.get_bucket(gcs_asset.bucket_name)
            blob = bucket.blob(blob_name=gcs_asset.key_name)
            local_asset_file = os.path.join(ctx.base_dir, gcs_asset.target_path)
            blob.download_to_filename(local_asset_file)
            handled_files.append(local_asset_file)
        return handled_files


class SomlierModelAsset(BaseSchema):
    provider: SomlierModelAssetProvider
    files: Dict[str, SomlierModelAssetFile]

    def download_or_provide(self, base_dir: str = os.getcwd()):
        handler = self.get_handler()
        return handler.handle(ctx=SomlierModelAssetHandlerContext(files=self.files, base_dir=base_dir))

    def get_handler(self) -> SomlierModelAssetHandler:
        concrete_subclasses = [subclass() for subclass in SomlierModelAssetHandler.__subclasses__()]
        handler_map = {subclass.provider: subclass for subclass in concrete_subclasses if subclass.provider}

        try:
            return handler_map[self.provider]
        except KeyError:
            raise ValueError("지원하지 않는 provider입니다")
