import os


def test_create_should_raise_error(somlier_cli_runner, tmpdir):
    output = somlier_cli_runner.run(
        args=["offline", "create", "wrong_docker_image", "'0 0 * * *'", "'make main.py'", "test_DAG", str(tmpdir)]
    )

    assert (
        output["error_message"] == "올바르지 않은 docker image input 입니다\n"
        "detail: {'title': '올바르지 않은 docker image input 입니다', "
        "'detail': 'docker-image: [wrong_docker_image]'}"
    )


def test_create_should_print_dag_file(somlier_cli_runner, tmpdir):
    dag_id = "test_DAG"
    file_path = f"{dag_id}.py"

    output = somlier_cli_runner.run(
        args=["offline", "create", "alpine:latest", "'0 0 * * *'", "'make main.py'", dag_id, str(tmpdir)]
    )

    assert f"{file_path}에 DAG가 생성되었습니다." in output
    assert os.path.isfile(tmpdir / file_path) is True
    assert "from datetime import datetime" in open(tmpdir / file_path).read()


def test_create_with_gpu_parameters_should_create_file(somlier_cli_runner, tmpdir):
    dag_id = "test_DAG"
    file_path = f"{dag_id}.py"

    output = somlier_cli_runner.run(
        args=[
            "offline",
            "create",
            "alpine:latest",
            "'0 0 * * *'",
            "'make main.py'",
            dag_id,
            str(tmpdir),
            "--gpu_type=nvidia-tesla-p100",
            "--num_of_gpus=1",
        ]
    )

    assert f"{file_path}에 DAG가 생성되었습니다." in output
    assert os.path.isfile(tmpdir / file_path) is True
    assert "from datetime import datetime" in open(tmpdir / file_path).read()
