from somlier.application.ports.clients.mlflow_client import MLflowRunNotFoundError
from somlier.application.use_cases.online.register.exceptions import (
    ArtifactNotFoundInGCSError,
    InvalidSklearnModelError,
    GitRepositoryNotFoundError,
    PytorchModuleFileNotFoundError,
    PytorchModuleClassNotFoundError,
    LoadPytorchWeightsRuntimeError,
    EmptyProjectParameterError,
)


def test_register_with_non_existing_run_id_should_raise_error(somlier_cli_runner_with_internal_service):
    output = somlier_cli_runner_with_internal_service.run(["online", "register", "run_id", "not_existing_project"])

    assert isinstance(output["error_class"], MLflowRunNotFoundError) is True


def test_register_v2_with_non_existing_gcs_uri(somlier_cli_runner_with_internal_service):
    """somlier online register_v2 수행을 위해 입력으로 받은 gcs_uri 경로에 파일 아티팩트가 존재하지 않을 때 에러 케이스를 테스트한다."""

    NON_EXISTING_GCS_URI = "gs://NON_EXISTING_GCS_URI"

    expected = ArtifactNotFoundInGCSError(title=f"모델 아티팩트 파일이 존재하지 않는 GCS URI입니다. [{NON_EXISTING_GCS_URI}]")
    output = somlier_cli_runner_with_internal_service.run(
        ["online", "register_v2", "sklearn", NON_EXISTING_GCS_URI, "model_name"]
    )
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)

    output = somlier_cli_runner_with_internal_service.run(
        [
            "online",
            "register_v2",
            "pytorch",
            NON_EXISTING_GCS_URI,
            "model_name",
            "github_uri",
            "project_name",
            "project_ref",
            "model_module_path",
            "model_class_name",
        ]
    )
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)


def test_register_v2_with_empty_github_uri(somlier_cli_runner_with_internal_service):
    """pytorch 모델을 등록하는 유즈케이스에서 github_uri가 입력되지 않을 때 에러 케이스를 테스트한다."""

    output = somlier_cli_runner_with_internal_service.run(
        [
            "online",
            "register_v2",
            "pytorch",
            "gs://socar-data-modeling/temp_serena/imu-driving-behavior-analysis/artifacts/ensemble_accident_based_weights_s700.pth",
            "model_name",
        ]
    )

    expected = EmptyProjectParameterError(
        title="pytorch 모델의 등록을 위해서는 모델 클래스가 정의된 github project repository 정보가 필요합니다."
    )
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)


def test_register_v2_with_invalid_sklearn_model(somlier_cli_runner_with_internal_service):
    """sklearn 모델을 등록하는 유즈케이스에서 올바르지 않은 형식의 아티팩트를 입력 받았을 때 에러 케이스를 테스트한다."""

    INVALID_SKLEARN_MODEL_GCS_URI = "gs://socar-data-modeling/temp_serena/mlops/UFL.txt"

    output = somlier_cli_runner_with_internal_service.run(
        ["online", "register_v2", "sklearn", INVALID_SKLEARN_MODEL_GCS_URI, "model_name"]
    )
    expected = InvalidSklearnModelError(title=f"joblib으로 로드할 수 있는 sklearn 모델 파일이 아닙니다.")
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)


def test_register_v2_with_non_existing_github_uri(somlier_cli_runner_with_internal_service):
    """pytorch 모델을 등록하는 유즈케이스에서 존재하지 않는 github uri를 입력 받았을 때 에러 케이스를 테스트한다."""

    NON_EXISTING_REPOSITORY = "git@github.com:socar-inc/NON_EXISTING_REPOSITORY.git"
    PROJECT_REf = "project_ref"

    output = somlier_cli_runner_with_internal_service.run(
        [
            "online",
            "register_v2",
            "pytorch",
            "gs://socar-data-modeling/temp_serena/imu-driving-behavior-analysis/artifacts/ensemble_accident_based_weights_s700.pth",
            "model_name",
            NON_EXISTING_REPOSITORY,
            "project_name",
            PROJECT_REf,
            "model_module_path",
            "model_class_name",
        ]
    )

    expected = GitRepositoryNotFoundError(
        title=f"존재하지 않는 Repository 또는 ref(branch)입니다. [{NON_EXISTING_REPOSITORY}, {PROJECT_REf}]"
    )
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)


def test_register_v2_with_non_existing_project_name(somlier_cli_runner_with_internal_service):
    """pytorch 모델을 등록하는 유즈케이스에서 존재하지 않는 project name를 입력 받았을 때 에러 케이스를 테스트한다."""

    NON_EXISTING_PROJECT_NAME = "NON_EXISTING_PROJECT_NAME"
    MODEL_MODULE_PATH = "model_module_path"

    output = somlier_cli_runner_with_internal_service.run(
        [
            "online",
            "register_v2",
            "pytorch",
            "gs://socar-data-modeling/temp_serena/imu-driving-behavior-analysis/artifacts/ensemble_accident_based_weights_s700.pth",
            "model_name",
            "git@github.com:socar-inc/socar-data-ml-projects.git",
            NON_EXISTING_PROJECT_NAME,
            "main",
            MODEL_MODULE_PATH,
            "model_class_name",
        ]
    )

    expected = PytorchModuleFileNotFoundError(
        title="Pytorch 모델의 모듈 경로를 찾을 수 없습니다.", detail=f"{NON_EXISTING_PROJECT_NAME}/{MODEL_MODULE_PATH}"
    )
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)


def test_register_v2_with_non_existing_model_module_path(somlier_cli_runner_with_internal_service):
    """pytorch 모델을 등록하는 유즈케이스에서 존재하지 않는 model module path를 입력 받았을 때 에러 케이스를 테스트한다."""

    PROJECT_NAME = "safe_driving_scoring"
    NON_EXISTING_MODEL_MODULE_PATH = "NON_EXISTING_MODEL_MODULE_PATH"

    output = somlier_cli_runner_with_internal_service.run(
        [
            "online",
            "register_v2",
            "pytorch",
            "gs://socar-data-modeling/temp_serena/imu-driving-behavior-analysis/artifacts/ensemble_accident_based_weights_s700.pth",
            "model_name",
            "git@github.com:socar-inc/socar-data-ml-projects.git",
            PROJECT_NAME,
            "main",
            NON_EXISTING_MODEL_MODULE_PATH,
            "model_class_name",
        ]
    )

    expected = PytorchModuleFileNotFoundError(
        title="Pytorch 모델의 모듈 경로를 찾을 수 없습니다.", detail=f"{PROJECT_NAME}/{NON_EXISTING_MODEL_MODULE_PATH}"
    )
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)


def test_register_v2_with_non_existing_model_class_name(somlier_cli_runner_with_internal_service):
    """pytorch 모델을 등록하는 유즈케이스에서 존재하지 않는 model class name를 입력 받았을 때 에러 케이스를 테스트한다."""

    output = somlier_cli_runner_with_internal_service.run(
        [
            "online",
            "register_v2",
            "pytorch",
            "gs://socar-data-modeling/temp_serena/imu-driving-behavior-analysis/artifacts/ensemble_accident_based_weights_s700.pth",
            "model_name",
            "git@github.com:socar-inc/socar-data-ml-projects.git",
            "safe_driving_scoring",
            "main",
            "models/lstm_classifier.py",
            "NON_EXISTING_MODEL_CLASS_NAME",
        ]
    )

    expected = PytorchModuleClassNotFoundError(
        title="Pytorch 모델의 클래스를 찾을 수 없습니다.",
        detail="safe_driving_scoring.models.lstm_classifier.NON_EXISTING_MODEL_CLASS_NAME",
    )
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)


def test_register_v2_with_unmatched_model_and_artifacts(somlier_cli_runner_with_internal_service):
    """pytorch 모델을 등록하는 유즈케이스에서 모델에 아티팩트(weights)를 로드할 수 없는 에러 케이스를 테스트한다."""

    output = somlier_cli_runner_with_internal_service.run(
        [
            "online",
            "register_v2",
            "pytorch",
            "gs://socar-data-modeling/temp_serena/imu-driving-behavior-analysis/artifacts/ensemble_accident_based_weights_s700.pth",
            "model_name",
            "git@github.com:socar-inc/socar-data-ml-projects.git",
            "safe_driving_scoring",
            "main",
            "models/lstm_classifier.py",
            "LSTMReservationClassifier",  # 이 모델의 아키텍쳐는 gcs uri에 업로드된 weights와 맞지 않는다. (서로 다른 모델)
        ]
    )

    expected = LoadPytorchWeightsRuntimeError(title="Pytorch 모델에 아티팩트를 정상적으로 로드하지 못했습니다.")
    assert isinstance(output["error_class"], expected.__class__) and output["error_message"] == str(expected)


def test_register_v2_with_success(somlier_cli_runner_with_internal_service):
    """정상적으로 작동하는 register_v2 케이스를 테스트한다."""

    output = somlier_cli_runner_with_internal_service.run(
        [
            "online",
            "register_v2",
            "pytorch",
            "gs://socar-data-modeling/temp_serena/imu-driving-behavior-analysis/artifacts/ensemble_accident_based_weights_s700.pth",
            "sts-drgps-acceleration-accident-risk",
            "git@github.com:socar-inc/socar-data-ml-projects.git",
            "safe_driving_scoring",
            "main",
            "models/lstm_classifier.py",
            "LSTMEnsembleReservationClassifier",
        ]
    )

    assert output == ""
