import os
from pathlib import Path
from typing import Optional, Tuple

from somlier.schema.config import SomlierSchema

SOMLIER_FILE_NAMES = {"somlier", "somlier.yaml", "somlier.yml"}


def find_somlier(base_dir: str = os.getcwd()) -> str:
    filenames = os.listdir(base_dir)
    for filename in filenames:
        if filename.lower() in SOMLIER_FILE_NAMES:
            return os.path.join(base_dir, filename)

    raise FileNotFoundError("SOMLIER config 'yaml'을 찾을 수 없습니다")


def load_somlier(base_dir: str = os.getcwd(), *, file_path: Optional[str] = None) -> Tuple[SomlierSchema, Path]:
    if not file_path:
        somlier_yaml = find_somlier(base_dir=base_dir)
        return SomlierSchema.from_yaml(somlier_yaml), Path(somlier_yaml).absolute()

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"SOMLIER config 'yaml'을 찾을 수 없습니다\n[file_path: {file_path}]")

    return SomlierSchema.from_yaml(file_path), Path(file_path).absolute()
