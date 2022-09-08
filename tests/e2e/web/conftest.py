import mlflow
import pytest
from fastapi.testclient import TestClient

from tests.utils.connection import can_access_internal_service

TEST_EXPERIMENT_NAME = "test_experiment"


@pytest.fixture(scope="session")
def client(somlier_test_container):
    app = somlier_test_container.server_app()
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture(scope="session")
def client_with_default_run(client):
    if not can_access_internal_service(timeout=1):
        pytest.skip("Cannot access internal service")
    existing_experiment = mlflow.get_experiment_by_name(TEST_EXPERIMENT_NAME)
    if not existing_experiment:
        experiment_id = mlflow.create_experiment(name=TEST_EXPERIMENT_NAME)
        with mlflow.start_run(experiment_id=experiment_id):
            mlflow.log_param("x", 1)
            mlflow.log_metric("y", 2)

    try:
        yield client
    finally:
        if existing_experiment.lifecycle_stage != "deleted":
            mlflow.delete_experiment(experiment_id=existing_experiment.experiment_id)
