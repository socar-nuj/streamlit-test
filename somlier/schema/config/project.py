from typing import Optional, List, Union, Tuple, Dict, Any

from pydantic import FilePath as LocalFilePath, Field

from somlier.schema.config.common import BaseSchema


class SomlierPythonMeta(BaseSchema):
    version: str
    requirements_txt: Optional[LocalFilePath]


class SomlierDockerMeta(BaseSchema):
    name: str
    tags: List[str] = Field(default=["latest"])
    volumes: List[str] = Field(default_factory=list)
    env: List[Union[str, Tuple[str, ...]]] = Field(default_factory=list)


class SomlierMLProject(BaseSchema):
    name: str
    python: SomlierPythonMeta
    docker: Optional[SomlierDockerMeta]

    @property
    def docker_env(self) -> Optional[Dict[str, Any]]:
        if not self.docker:
            return None
        return {"image": self.docker.name, "volumes": self.docker.volumes, "environment": self.docker.env}
