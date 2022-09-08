from pathlib import Path

from pydantic import BaseSettings, Field, FilePath

from somlier.core.pydantic import DefaultSettings

_here = Path(__file__).parent


class MLflowRESTConfig(DefaultSettings):
    tracking_uri: str = Field(default="", env="SOMLIER__MLFLOW__TRACKING_URI")
    kube_context: str = Field(default="gke_socar-data-dev_us-east1-b_socar-ml-us-east1-b-dev-cluster")
    kube_config_path: str = Field(default="", env="SOMLIER__MLFLOW__KUBE_CONFIG_PATH")
    kube_repository_uri: str = Field(default="", env="SOMLIER__MLFLOW__KUBE_REPOSITORY_URI")
    kube_job_template_path: FilePath = Field(
        default=f"{_here}/kubernetes_job_template.yaml", env="SOMLIER__MLFLOW__JOB_TEMPLATE_PATH"
    )
    kube_job_with_gpu_template_path: FilePath = Field(
        default=f"{_here}/kubernetes_job_with_gpu_template.yaml", env="SOMLIER__MLFLOW__JOB_WITH_GPU_TEMPLATE_PATH"
    )


class MLflowConfig(BaseSettings):
    rest: MLflowRESTConfig = Field(default_factory=MLflowRESTConfig)
    default_project_uri: str = Field(default="", env="SOMLIER__MLFLOW__DEFAULT_PROJECT_URI")
