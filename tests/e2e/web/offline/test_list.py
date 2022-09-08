def test_rest_offline_list_should_get_valid_dag_list(client_with_default_run):
    # when
    response = client_with_default_run.get("/offline/list", json={})

    # then
    assert response.status_code == 200
    assert any(response.json())
