import pytest

from somlier.external_interfaces.exceptions import ConnectionTimeoutError
from tests.utils.connection import can_access_internal_service

TEST_MLFLOW_TRACKING_SERVER_URI = "http://mlflow.mlops.socar.me"

EXISTING_MODEL_NAME = "example-project"


@pytest.mark.skipif(can_access_internal_service(timeout=1) is False, reason="VPN Connection is not available")
def test_get_when_model_does_not_exist(somlier_test_container):
    repository = somlier_test_container.online_container.container.model_repository()
    result = repository.find_by_model_name_and_version(model_name="NOT_EXISTING_MODEL_NAME", model_version="1")
    assert result is None


@pytest.mark.skipif(
    can_access_internal_service(timeout=1) is True,
    reason="mlflow tracking server에 접근하지 못할 때를 핸들링하기 위한 테스트 입니다. VPN 연결을 끄고 테스트 해주세요.",
)
def test_get_when_mlflow_tracking_server_is_unreachable(somlier_test_container):
    with pytest.raises(ConnectionTimeoutError):
        repository = somlier_test_container.online_container.container.model_repository()
        repository.find_by_model_name_and_version(model_name=EXISTING_MODEL_NAME, model_version="1")


@pytest.mark.skipif(can_access_internal_service(timeout=1) is False, reason="VPN Connection is not available")
def test_get(somlier_test_container):
    repository = somlier_test_container.online_container.container.model_repository()
    repository.find_by_model_name_and_version(model_name=EXISTING_MODEL_NAME, model_version="1")
