def test_local_deploy_not_implemented_error(client):
    # when
    response = client.post("/online/deploy", json={"model_name": "fake_model", "model_version": "1", "use_k8s": False})

    # then
    assert response.status_code == 501
