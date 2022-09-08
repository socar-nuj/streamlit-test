def test_invalid_request_with_wrong_run_id(client_with_default_run):
    response = client_with_default_run.post(
        "/online/register",
        json={
            "run_id": "wrong run id",
            "model_name": "example-projects/sklearn",
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "status_code": 422,
        "title": "run_id 값이 유효하지 않습니다",
        "detail": "Invalid run ID: 'wrong run id'",
    }


# TODO: 아래 테스트들은 통합 테스트 환경이 만들어진 이후에 작업할 예정입니다.

"""
TODO(hardy): run_id가 유효하고, model_name이 이미 기존에 있는 경우의 테스트
-> 기존에 등록된 모델 'model_name'의 버전이 올라가야 한다.
"""

"""
TODO(hardy): run_id가 유효하고, model_name이 기존에 없는 경우의 테스트
-> 새로운 모델 'model_name'을 등록해야 한다.
"""

"""
TODO(hardy): run_id가 유효하고, model_name이 기존에 있는데, 이미 등록된 모델 버전인 경우
-> 기존에 등록된 모델 버전을 반환해야 한다.
"""
