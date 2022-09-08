from somlier.application.use_cases.online.search import MLflowProjectNotFoundError


def test_search_request_with_wrong_project_name_should_raise_error(somlier_cli_runner_with_internal_service):
    output = somlier_cli_runner_with_internal_service.run(["online", "search", "wrong_name", "rmse", "false"])

    assert isinstance(output["error_class"], MLflowProjectNotFoundError) is True
