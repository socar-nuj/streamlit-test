import os
from enum import Enum

import pytest

from somlier.config import AirflowConfig, AppConfig, MLflowConfig
from somlier.config.airflow import AirflowRESTConfig
from somlier.config.mlflow import MLflowRESTConfig
from somlier.external_interfaces.container import create_container


class TestEnvironment(Enum):
    LOCAL = "local"
    COMPOSE = "compose"


TEST_ENV: TestEnvironment = TestEnvironment(os.getenv("TEST_ENV", "local"))
TEST_CONFIG = AppConfig(
    mlflow=MLflowConfig(
        rest=MLflowRESTConfig(
            tracking_uri="http://mlflow.mlops.socar.me"
            if TEST_ENV == TestEnvironment.LOCAL
            else "http://tracking_server:5000"
        ),
        default_project_uri="https://github.com/socar-inc/socar-data-ml-projects.git",
    ),
    airflow=AirflowConfig(rest=AirflowRESTConfig(host="http://airflow.mlops.socar.me")),
)


@pytest.fixture(scope="session")
def somlier_test_container():
    return create_container(config=TEST_CONFIG)
