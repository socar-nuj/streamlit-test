import json
import os
import tempfile
from typing import Optional, Tuple

import requests
from git import Repo
from jinja2 import Environment, FileSystemLoader
from loguru import logger
from pydantic import BaseModel, Field

from somlier.application.constants import ROOT_PATH
from somlier.application.exceptions import InvalidParameterError, NotFoundError
from somlier.application.ports.clients.airflow_client import AirflowClient
from somlier.application.ports.clients.dag_builder_client import DAGBuilderClient


class CreateBatchRequest(BaseModel):
    docker_image: str
    schedule: str
    entrypoint: str
    # is_dry_run: bool = Field(default=False)
    dag_id: Optional[str] = Field(default="test_dag")
    target_dir: Optional[str] = Field(default=None)
    gpu_type: Optional[str] = Field(default="nvidia-tesla-p100")
    num_of_gpus: Optional[int]


# TODO(serena): Data Validation
class CreateBatchRequestV2(BaseModel):
    model_ref: str
    dag_id: str
    schedule_interval: str
    start_date: str
    dataset_ref: str
    dataset_load_column: str
    dataset_load_by_kst: bool
    dataset_load_window: int
    destination_table_ref: str
    github_personal_access_token: str


class CreateBatchResponse(BaseModel):
    dag: str


class CreateBatchResponseV2(BaseModel):
    remote_dag_ref: str
    msg: str


class AirflowDAGNotFoundError(NotFoundError):
    pass


class InvalidTargetDirectoryError(InvalidParameterError):
    pass


class RequiredPackageNotFound(NotFoundError):
    pass


class CreateBatch:
    def __init__(
        self, airflow_client: AirflowClient, mlops_dag_repo_url: str, dag_builder_client: DAGBuilderClient
    ) -> None:
        self.airflow_client = airflow_client
        self.mlops_dag_repo_url = mlops_dag_repo_url
        self.dag_builder_client = dag_builder_client

    def execute(self, request: CreateBatchRequest) -> CreateBatchResponse:
        if not self.dag_builder_client.can_use:
            raise RequiredPackageNotFound(
                title="offline create use_case에 필요한 패키지를 찾을 수 없습니다",
                detail="'poetry install --extras offline'으로 관련 패키지를 설치해주세요",
            )

        result = self._execute_create(**request.dict())
        return CreateBatchResponse(dag=result)

    def _execute_create(
        self,
        docker_image: str,
        schedule: str,
        entrypoint: str,
        dag_id: str,
        template: str = "mlops",
        target_dir: Optional[str] = None,
        gpu_type: Optional[str] = "nvidia-tesla-p100",
        num_of_gpus: Optional[int] = None,
    ) -> str:
        """
        Batch Usecase - Create을 실행합니다

        Returns:
            str: airflow dag file string

        Raises:
            InvalidTargetDirectoryError: 타겟 디렉토리를 찾을 수 없는 경우
        """
        # NOTE: airflow DAG를 Git repo에 올리는 액션을 사용자에게 위임합니다. 해당 맥락은 아래 링크에서 확인할 수 있습니다.
        # https://www.notion.so/socarcorp/Offline-Serving-3a7e7e482d8e45e2b3a99a58eff59109
        #
        # can_use_directory = os.path.isdir(directory) and os.path.exists(directory)
        # if not can_use_directory:
        #     raise InvalidTargetDirectoryError(title=f"[{directory}] 디렉토리를 이용할 수 없습니다")
        #
        # repo = Repo.clone_from(url=self.mlops_dag_repo_url, to_path=directory)
        # logger.info(f"[{directory}]에 DAG Repo를 클론했습니다")

        try:
            return self.dag_builder_client.generate(
                args=[
                    "generate",
                    docker_image,
                    f"'{schedule}'",
                    f"'{entrypoint}'",
                    dag_id,
                    template,
                    *([f"--gpu-type={gpu_type}", f"--num-of-gpus={num_of_gpus}"] if gpu_type and num_of_gpus else []),
                ]
            )
        except Exception as e:
            raise e


class CreateBatchV2:
    def __init__(
        self, airflow_client: AirflowClient, mlops_dag_repo_url: str, dag_builder_client: DAGBuilderClient
    ) -> None:
        self.airflow_client = airflow_client
        self.mlops_dag_repo_url = mlops_dag_repo_url
        self.dag_builder_client = dag_builder_client

    def execute(self, request: CreateBatchRequestV2) -> CreateBatchResponseV2:
        if not self.dag_builder_client.can_use:
            raise RequiredPackageNotFound(
                title="offline create use_case에 필요한 패키지를 찾을 수 없습니다",
                detail="'poetry install --extras offline'으로 관련 패키지를 설치해주세요",
            )

        with tempfile.TemporaryDirectory() as tmpdir:
            remote_dag_ref, msg = self._execute_create(
                directory=tmpdir, **request.dict(exclude={"subcommand", "target_directory"})
            )
        return CreateBatchResponseV2(remote_dag_ref=remote_dag_ref, msg=msg)

    def _execute_create(
        self,
        model_ref: str,
        dag_id: str,
        schedule_interval: str,
        start_date: str,
        dataset_ref: str,
        dataset_load_column: str,
        dataset_load_by_kst: bool,
        dataset_load_window: int,
        destination_table_ref: str,
        github_personal_access_token: str,
        directory: str,
    ) -> Tuple[str, str]:
        can_use_directory = os.path.isdir(directory) and os.path.exists(directory)
        if not can_use_directory:
            raise InvalidTargetDirectoryError(title=f"[{directory}] 디렉토리를 이용할 수 없습니다.")

        # socar-data-mlops-dags Repo를 클론하고, PR을 만들기 위한 브랜치를 checkout합니다.
        repo = Repo.clone_from(url=self.mlops_dag_repo_url, to_path=directory)
        base_branch_name = repo.active_branch.name
        logger.info(f"[{directory}]에 DAG Repo({self.mlops_dag_repo_url})를 클론했습니다.")

        branch_name = f"somlier/{dag_id.replace('_', '-')}"
        repo.git.checkout("-b", branch_name)

        if branch_name in repo.remote("origin").refs:
            repo.remote("origin").pull(branch_name)  # 이미 리모트 저장소에 동일 브랜치가 존재하는 경우 pull합니다.

        logger.info(f"브랜치 [{branch_name}]을 생성했습니다.")

        # DAG 파일을 저장합니다.
        dag_saved_path = self._render_dag_template(
            model_ref,
            dag_id,
            schedule_interval,
            start_date,
            dataset_ref,
            dataset_load_column,
            dataset_load_by_kst,
            dataset_load_window,
            destination_table_ref,
            directory,
        )

        # 생성된 DAG 파일에 대해서 add, commit, push합니다.
        repo.index.add(dag_saved_path)
        repo.index.commit(f"feat(dags/{dag_id}): {dag_id}를 추가한다")
        info = repo.remote("origin").push(branch_name)
        remote_dag_ref = info[0].remote_ref_string
        logger.info(f"DAG 파일을 리모트 저장소에 저장했습니다. 위치: [{remote_dag_ref}]")

        # Pull Request을 생성합니다.
        is_success, msg = self._create_pull_request(
            pr_title=f"feat(dags/{dag_id}): {dag_id}를 추가한다",
            branch_name=branch_name,
            base_branch_name=base_branch_name,
            github_personal_access_token=github_personal_access_token,
        )

        if is_success:
            logger.info(f"Pull Request 생성이 완료되었습니다. 위치: [{msg}]")
        else:
            logger.error(f"Pull Request 생성이 실패하였습니다. 사유: [{msg}]")

        return remote_dag_ref, msg

    def _render_dag_template(
        self,
        model_ref: str,
        dag_id: str,
        schedule_interval: str,
        start_date: str,
        dataset_ref: str,
        dataset_load_column: str,
        dataset_load_by_kst: bool,
        dataset_load_window: int,
        destination_table_ref: str,
        directory: str,
    ) -> str:
        """DAG .py 파일을 렌더링합니다."""

        # TODO(serena): 아래 템플릿 기준으로 socar-data-dag-builder에 기능 추가하는 것은 험프리와 다시 논의해야 합니다.
        try:
            env = Environment(
                loader=FileSystemLoader(f"{ROOT_PATH}/jinja_templates"),
            )
            template = env.get_template("socar_data_provider_template.j2")
            rendered = template.render(
                dag_id=dag_id,
                description=f"somlier offline create_v2을 통해 생성된 DAG {dag_id}",
                start_date=start_date,
                schedule_interval=schedule_interval,
                model_name=model_ref.split("/")[0],
                model_version=model_ref.split("/")[1],
                dataset_ref=dataset_ref,
                dataset_load_column=dataset_load_column,
                dataset_load_by_kst=dataset_load_by_kst,
                dataset_load_window=dataset_load_window - 1,  # execution date로 이미 하루 딜레이가 있으니 -1 해준다
                destination_table_ref=destination_table_ref,
            )
        except Exception as e:
            raise e

        dag_saved_dir = os.path.join(directory, "dags")
        if not os.path.exists(dag_saved_dir):
            os.makedirs(dag_saved_dir)

        dag_saved_path = os.path.join(dag_saved_dir, f"{dag_id}.py")
        with open(dag_saved_path, "w") as file:
            file.write(rendered)
        logger.info(f"DAG 파일을 생성했습니다. 위치: [{dag_saved_path}]")

        return dag_saved_path

    def _create_pull_request(
        self, pr_title: str, branch_name: str, base_branch_name: str, github_personal_access_token: str
    ) -> Tuple[bool, str]:
        """특정 브랜치의 작업 결과에 대해 master 브랜치에 Pull Request을 생성합니다."""

        owner = self.mlops_dag_repo_url.split("/")[-2]
        repo_name = self.mlops_dag_repo_url.split("/")[-1].replace(".git", "")

        # TODO(serena): outbound/rest의 하나의 port로 만들기
        data = {
            "title": pr_title,
            "head": branch_name,
            "base": base_branch_name,
        }
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {github_personal_access_token}",
        }
        resp = requests.post(
            f"https://api.github.com/repos/{owner}/{repo_name}/pulls",
            headers=headers,
            data=json.dumps(data),
        )
        logger.info(f"Pull Request 생성을 요청하였습니다. 응답: [{resp.status_code}]")
        response_txt = json.loads(resp.text)

        if resp.status_code == 201:
            try:
                return True, response_txt["html_url"]
            except KeyError:
                return (
                    False,
                    response_txt,
                )  # API 문서상 return code == 201은 성공 상태로 html_url 속성을 가지나, 발생할 수 있는 에러 대비를 위해 key error 추가
        else:
            return False, response_txt["errors"]
