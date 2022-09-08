from somlier.application.ports.clients.mlflow_client import MLProjectNotFoundError
from somlier.application.use_cases.online.train.exceptions import (
    InvalidParamsFormatError,
    InvalidContinuousParamError,
    EmptyParamsError,
)


def test_train_request_with_wrong_project_name_should_raise_error(somlier_cli_runner_with_internal_service):
    output = somlier_cli_runner_with_internal_service.run(
        args=["online", "train", "wrong_project", "main"]
    )  # NOTE(humphrey): 핸들링되지 않은 attribute 에러가 난다

    assert isinstance(output["error_class"], MLProjectNotFoundError)


def test_train_request_with_wrong_continuous_parameter_format(somlier_cli_runner_with_internal_service):
    """파라미터를 주입하는 유즈케이스에서 올바르지 않은 형태로 연속형 파라미터가 들어갔을 때의 에러 케이스를 테스트한다."""

    INVALID_PARAM_FORMAT = "1..10"  # increment 값이 들어오지 않았을 때
    output = somlier_cli_runner_with_internal_service.run(
        args=[
            "online",
            "train",
            "example-projects/torch-fashion-mnist",
            "docker-image-platform-build",
            "--github_uri=git@github.com:socar-inc/socar-data-ml-projects.git",
            f"--batch_size={INVALID_PARAM_FORMAT}",
        ]
    )

    expected = InvalidParamsFormatError(
        title=f"올바른 파라미터 형태가 아닙니다. [{INVALID_PARAM_FORMAT.split('=')[-1]}]",
        detail="Required: type=start..end..increment or type=value1,value2,value3 or type=value",
    )
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)


def test_train_request_with_wrong_continuous_parameter_type(somlier_cli_runner_with_internal_service):
    """파라미터를 주입하는 유즈케이스에서 올바르지 않은 연속형 파라미터가 들어갔을 때의 에러 케이스를 테스트한다."""

    INVALID_PARAM_FORMAT = "A..B..C"  # 불연속형 파라미터를 연속형 포맷으로 넣었을 때
    output = somlier_cli_runner_with_internal_service.run(
        args=[
            "online",
            "train",
            "example-projects/torch-fashion-mnist",
            "docker-image-platform-build",
            "--github_uri=git@github.com:socar-inc/socar-data-ml-projects.git",
            f"--batch_size={INVALID_PARAM_FORMAT}",
        ]
    )

    expected = InvalidParamsFormatError(
        title=f"올바른 파라미터 형태가 아닙니다. [{INVALID_PARAM_FORMAT.split('=')[-1]}]",
        detail="Required: type=start..end..increment or type=value1,value2,value3 or type=value",
    )
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)


def test_train_request_with_wrong_continuous_parameter_increment(somlier_cli_runner_with_internal_service):
    """파라미터를 주입하는 유즈케이스에서 연속형 타입에 대해 올바르지 않은 start, end, increment값이 들어왔을 때의 에러 케이스를 테스트한다."""

    INVALID_PARAM_FORMAT = "10..1..2"  # start=10, end=1, increment=2로 올바르지 않음
    output = somlier_cli_runner_with_internal_service.run(
        args=[
            "online",
            "train",
            "example-projects/torch-fashion-mnist",
            "docker-image-platform-build",
            "--github_uri=git@github.com:socar-inc/socar-data-ml-projects.git",
            f"--batch_size={INVALID_PARAM_FORMAT}",
        ]
    )

    expected = InvalidContinuousParamError(title="잘못된 연속형 파라미터 값입니다.")
    assert isinstance(output["error_class"], expected.__class__)


def test_train_request_with_empty_parameter_condition(somlier_cli_runner_with_internal_service):
    """파라미터를 주입하는 유즈케이스에서 조건에 일치하는 파라미터가 없을 때의 에러 케이스를 테스트한다."""

    INVALID_PARAM_FORMAT = "1..1..1"  # [1, 1)에는 정수값이 존재하지 않음
    output = somlier_cli_runner_with_internal_service.run(
        args=[
            "online",
            "train",
            "example-projects/torch-fashion-mnist",
            "docker-image-platform-build",
            "--github_uri=git@github.com:socar-inc/socar-data-ml-projects.git",
            f"--batch_size={INVALID_PARAM_FORMAT}",
        ]
    )

    expected = EmptyParamsError(title=f"조건에 일치하는 파라미터가 없습니다. [batch_size]")
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)
