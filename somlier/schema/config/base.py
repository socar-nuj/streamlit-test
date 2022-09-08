import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import yaml
from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements
from pip._internal.req.req_file import ParsedRequirement
from pydantic import Field, PrivateAttr, ValidationError

from somlier.application.use_cases.config.exceptions import SomlierValidationError
from somlier.config import configure
from somlier.config.configure import FilePath
from somlier.schema.config.assets import SomlierModelAsset
from somlier.schema.config.common import BaseSchema
from somlier.schema.config.entrypoint import SomlierEntrypoint
from somlier.schema.config.global_config import SomlierGlobalConfig
from somlier.schema.config.model import SomlierModel
from somlier.schema.config.project import SomlierMLProject


class SomlierSchema(BaseSchema):
    global_config: SomlierGlobalConfig = Field(alias="global", default_factory=SomlierGlobalConfig)
    project: SomlierMLProject
    model: SomlierModel
    entrypoints: Dict[str, SomlierEntrypoint] = Field(default_factory=dict)

    _asset_dir: str = PrivateAttr(default="assets")

    @classmethod
    def from_yaml(cls, yaml_file: FilePath) -> "SomlierSchema":
        try:
            yaml_struct = configure(yaml_file, as_struct=True)
            somlier = cls(**yaml_struct.dict())
            somlier.validate_()
            return somlier
        except ValidationError as e:
            raise SomlierValidationError(f"Valid 하지 않은 somlier.yaml 파일 입니다\ndetail: {e.json()}")

    def to_yaml(self, base_dir: str = Path("."), yaml_file_name: str = "somlier.yaml") -> None:
        yaml_file_to_write = Path(os.path.join(base_dir, yaml_file_name))
        if yaml_file_to_write.exists():
            raise FileExistsError(f"{yaml_file_name}이 존재합니다")

        payload = json.loads(self.json())
        with open(yaml_file_to_write, "w") as f:
            try:
                yaml.safe_dump(payload, f)
            except yaml.representer.RepresenterError as e:
                os.unlink(yaml_file_to_write)
                raise e

    @property
    def env(self) -> str:
        return self.global_config.env

    @property
    def assets(self) -> List[SomlierModelAsset]:
        return self.model.assets

    @property
    def mlflow_meta(self) -> Dict[str, Any]:
        project_name = self.model.name
        docker_env = {"docker_env": self.project.docker_env} if self.project.docker_env else {}
        entrypoint = {
            "entrypoints": {
                entrypoint_name: entrypoint.dict(exclude_unset=True)
                for entrypoint_name, entrypoint in self.entrypoints.items()
            }
            if self.entrypoints
            else {}  # FIXME
        }
        return {"name": project_name, **docker_env, **entrypoint}

    @property
    def asset_names(self) -> List[str]:
        return [str(item) for asset in self.assets for item in asset.files.values()]

    @property
    def asset_dir(self) -> str:
        return os.path.abspath(self._asset_dir)

    @property
    def dependencies(self) -> List[ParsedRequirement]:
        return [
            req for req in parse_requirements(self.project.python.requirements_txt.name, session=PipSession()) if req
        ]

    def set_asset_dir(self, val: str) -> None:
        if not os.path.isdir:
            raise NotADirectoryError()
        self._asset_dir = val

    def add_asset(self, asset_entry: SomlierModelAsset) -> None:
        if any([asset_name for asset_name in asset_entry.files.keys() if asset_name in self.asset_names]):
            raise ValueError("같은 이름의 asset이 존재합니다.")
        self.model.assets.append(asset_entry)

    def prepare(self):
        if self.env == "TEST":
            return

        prepared_assets = []
        for asset in self.assets:
            downloaded_assets = asset.download_or_provide(self.asset_dir)
            prepared_assets += downloaded_assets
        return prepared_assets

    def create_mlflow_meta(self, base_dir: str = os.getcwd()) -> str:
        save_path = os.path.join(base_dir, "MLProject")
        with open(save_path, "w") as f:
            yaml.safe_dump(data=self.mlflow_meta, stream=f)
        return save_path

    def check_model_version_matches_project_version(self, pyproject_toml_path: str) -> bool:
        if not os.path.exists(pyproject_toml_path):
            raise ValueError()
        return False

    def validate_(self):
        for key, entrypoint in self.entrypoints.items():
            validated = entrypoint.validate_()
            if not validated:
                raise SomlierValidationError(f"[{key}] entrypoint가 올바르지 않습니다")
        return True

    def get_log_handler(self):
        log_format = self.global_config.logging.format
        if log_format == "json":

            def handler(stdout_line: str, name: str) -> str:
                entry = {"name": name, "stdout": stdout_line, "timestamp": datetime.now().isoformat()}
                return json.dumps(entry) + "\n"

        elif log_format == "text":

            def handler(stdout_line: str, name: str) -> str:
                return f"{name} | {datetime.now().isoformat()} | {stdout_line}"

        else:
            raise ValueError("logging format이 올바르지 않습니다.")

        return handler
