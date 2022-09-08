import os

import pytest

from tests.utils.connection import can_access_internal_service

INVALID_AIRFLOW_URL = "WRONG_URL"
VALID_AIRFLOW_URL = "http://airflow.mlops.socar.me"
VALID_USERNAME = os.getenv("AIRFLOW_USERNAME", "admin")
VALID_PASSWORD = os.getenv("AIRFLOW_PASSWORD", "socar")


@pytest.mark.skipif(can_access_internal_service(timeout=1) is False, reason="VPN Connection is not available")
def test_airflow_client_with_wrong_dag_id_should_raise_retry_error(somlier_test_container):
    client = somlier_test_container.offline_container.container.airflow_client()
    client.find_dag(dag_id="NON_EXISTING")
