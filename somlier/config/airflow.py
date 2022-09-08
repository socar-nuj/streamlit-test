import base64
from typing import Any, Dict

from pydantic import BaseSettings, Field

from somlier.core.pydantic import DefaultSettings


class AirflowRESTConfig(DefaultSettings):
    host: str = Field(default="", env="SOMLIER__AIRFLOW__HOST")
    username: str = Field(default="", env="SOMLIER__AIRFLOW__USERNAME")
    password: str = Field(default="", env="SOMLIER__AIRFLOW__PASSWORD")
    timeout: int = Field(default=5, env="SOMLIER__AIRFLOW__TIMEOUT")

    @property
    def headers(self) -> Dict[str, Any]:
        return {
            "Authorization": f"Basic {base64.b64encode(f'{self.username}:{self.password}'.encode('utf-8')).decode('utf-8')}"
        }


class AirflowConfig(BaseSettings):
    rest: AirflowRESTConfig = Field(default_factory=AirflowRESTConfig)
    default_dag_repo_url: str = Field(
        default="https://github.com/socar-inc/socar-data-mlops-dags", env="SOMLIER__AIRFLOW__DAG_REPO_URL"
    )
