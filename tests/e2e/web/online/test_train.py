def test_invalid_request_with_wrong_project_name(client_with_default_run):
    # when
    response = client_with_default_run.post(
        "/online/train", json={"project_name": "wrong project name", "project_ref": "main", "use_k8s_job": False}
    )

    # then
    for k, v in {"status_code": 404, "title": "해당하는 프로젝트가 존재하지 않습니다."}.items():
        assert response.json()[k] == v


def test_invalid_request_with_wrong_project_ref(client_with_default_run):
    # when
    response = client_with_default_run.post(
        "/online/train", json={"project_name": "default", "project_ref": "wrong_ref", "use_k8s_job": False}
    )

    # then
    assert response.status_code == 404
    for k, v in {"status_code": 404, "title": "해당하는 프로젝트의 버전이 존재하지 않습니다."}.items():
        assert response.json()[k] == v


# NOTE: mlflow와 git repo에 dependency가 있어서 해당 테스트가 돌아가면 사이드 이펙트 때문에 comment out 시킵니다
# def test_request_with_valid_request(client_with_default_run):
#     response = client_with_default_run.post(
#         "/online/train", json={"project_name": "humphrey-test", "project_ref": "humphrey-test", "use_k8s_job": False}
#     )
#
#     assert response.status_code == 200
