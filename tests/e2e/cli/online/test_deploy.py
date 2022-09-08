from somlier.application.use_cases.online.deploy import ModelNotFoundError

VERSION_THAT_SHOULD_NOT_EXIST = 999999999999


def test_deploy_non_existing_model_should_raise_error(somlier_cli_runner_with_internal_service):
    output = somlier_cli_runner_with_internal_service.run(args=["online", "deploy", "non_existing_model", "1"])

    assert isinstance(output["error_class"], ModelNotFoundError)


def test_deploy_non_existing_model_version_should_raise_error(somlier_cli_runner_with_internal_service):
    output = somlier_cli_runner_with_internal_service.run(
        args=["online", "deploy", "example-project", str(VERSION_THAT_SHOULD_NOT_EXIST)]
    )

    assert isinstance(output["error_class"], ModelNotFoundError)
