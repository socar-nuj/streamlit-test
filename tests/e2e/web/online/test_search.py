from tests.e2e.web.conftest import TEST_EXPERIMENT_NAME


def test_invalid_request_with_wrong_project_name(client_with_default_run):
    # when
    response = client_with_default_run.post(
        "/online/search",
        json={"project_name": "wrong project name", "metric_by": "training_mae", "ascending": False},
    )

    # then
    assert response.status_code == 404
    assert response.json() == {
        "detail": "",
        "status_code": 404,
        "title": "요청 내용 중 project_name 에 해당하는 프로젝트를 찾을 수 없습니다.",
    }


def test_invalid_request_with_wrong_standard_metric(client_with_default_run):
    # when
    response = client_with_default_run.post(
        "/online/search",
        json={"project_name": TEST_EXPERIMENT_NAME, "metric_by": "wrong value", "ascending": False},
    )

    # then
    assert response.status_code == 422
    assert response.json()["title"] == "metric 값이 유효하지 않습니다."
