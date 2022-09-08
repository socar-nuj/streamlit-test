from typing import Any, Dict, List, Union

import pytest

from somlier.external_interfaces.inbound.cli import MainController
from tests.utils.connection import can_access_internal_service


@pytest.fixture
def somlier_cli_test_controller(somlier_test_container):
    controller = MainController(container=somlier_test_container)
    return controller


@pytest.fixture
def somlier_cli_runner(somlier_cli_test_controller, capsys):
    import fire

    class _Runner:
        def run(self, args: List[str]) -> Union[Dict[str, Any], str]:
            try:
                fire.Fire(somlier_cli_test_controller, args, name="somlier_test_cli")
            except Exception as exc:
                output = {"error_class": exc, "error_message": str(exc)}
                return output
            captured = capsys.readouterr()
            result = captured.out
            return result

    return _Runner()


@pytest.fixture
def somlier_cli_runner_with_internal_service(somlier_cli_runner):
    if not can_access_internal_service(timeout=1):
        pytest.skip("Cannot access internal service")
    return somlier_cli_runner
