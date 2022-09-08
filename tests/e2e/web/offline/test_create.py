import pytest


@pytest.mark.skip("CI testing failure")
def test_rest_offline_create_request_with_valid_docker_image_should_pass(client):
    # when
    response = client.post(
        "/offline/create",
        json={
            "docker_image": "gcr.io/socar-data-dev/humphrey-test:latest",
            "schedule": "@once",
            "entrypoint": "echo hello world",
            "dag_id": "test_dag",
        },
    )

    # then
    assert response.status_code == 200
    assert "from datetime import datetime" in response.content.decode()


def test_rest_offline_create_request_with_invalid_docker_image_should_respond_500(client):
    # when
    response = client.post(
        "/offline/create",
        json={
            "docker_image": "NON_EXISTING",
            "schedule": "@once",
            "entrypoint": "echo hello world",
            "is_dry_run": True,
        },
    )
    # then
    assert response.status_code == 500
