from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from pytz import timezone

from somlier.application.use_cases.offline.create import (
    CreateBatchRequest,
    CreateBatchRequestV2,
)
from somlier.application.use_cases.offline.list import ListBatchesRequest
from somlier.external_interfaces.container import OfflineContainer


class OfflineController:
    def __init__(self, container: OfflineContainer) -> None:
        self.container = container

    def create(
        self,
        docker_image: str,
        schedule: str,
        entrypoint: str,
        dag_id: str,
        target_dir: str = str(Path(".")),
        gpu_type: Optional[str] = "nvidia-tesla-p100",
        num_of_gpus: Optional[int] = None,
    ) -> str:
        """
        Batch 서빙을 위해 Airflow DAG를 만들고, 배포합니다.

        Args:
            docker_image (str): 도커 이미지 (e.g., gcr.io/socar-data-dev/sift:latest)
            schedule (str): Airflow schedule expression (e.g., 0 0 * * *)
            entrypoint (str): 컨테이너의 entrypoint (e.g., sh -c predict.sh, make predict)
            dag_id (str): DAG id (주의: unique 해야합니다)
            target_dir (str): 파일을 만들 타겟 디렉토리 (default: 현재 경로)
            gpu_type (str): gpu type (e.g., nvidia-tesla-p100)
            num_of_gpus (int): gpu 장 수

        Returns:
            message (str)

        Raises:
            NotImplementedError: subcommand에 등록되지 않은 값이 입력된 경우
        """
        try:
            import dag_builder
        except ImportError:
            raise NotImplementedError("batch usecase를 실행할 수 없습니다")

        request = CreateBatchRequest(
            docker_image=docker_image,
            schedule=schedule,
            entrypoint=entrypoint,
            dag_id=dag_id,
            target_dir=target_dir,
            gpu_type=gpu_type,
            num_of_gpus=num_of_gpus,
        )

        use_case = self.container.create()
        response = use_case.execute(request=request)

        dag_path = Path(target_dir) / f"{dag_id}.py"
        with open(dag_path, "w") as file:
            file.write(response.dag)

        return f"{dag_path}에 DAG가 생성되었습니다."

    def create_v2(
        self,
        model_ref: str,
        dag_id: str,
        schedule_interval: str,
        dataset_ref: str,
        dataset_load_column: str,
        destination_table_ref: str,
        github_personal_access_token: str,
        start_date: str = (datetime.now(timezone("Asia/Seoul")) - timedelta(days=1)).strftime("%Y-%m-%d"),
        dataset_load_window: int = 1,
        dataset_load_by_kst: bool = True,
    ):
        """socar-airflow-data-provider를 이용해 배치 서빙을 자동화합니다. 모델은 MLflow에 register되어 있다고 가정합니다."""
        try:
            import dag_builder
        except ImportError:
            raise NotImplementedError("batch usecase를 실행할 수 없습니다")

        request = CreateBatchRequestV2(
            model_ref=model_ref,
            dag_id=dag_id,
            schedule_interval=schedule_interval,
            start_date=start_date,
            dataset_ref=dataset_ref,
            dataset_load_column=dataset_load_column,
            dataset_load_by_kst=dataset_load_by_kst,
            dataset_load_window=dataset_load_window,
            destination_table_ref=destination_table_ref,
            github_personal_access_token=github_personal_access_token,
        )

        use_case = self.container.create_v2()
        response = use_case.execute(request=request)

        return f"DAG 파일을 리모트 저장소에 저장했습니다. 위치: [{response.remote_dag_ref}]"

    def list(self) -> List[str]:
        """배포된 에어플로우 DAG 목록을 보여줍니다."""

        request = ListBatchesRequest()
        use_case = self.container.list()
        response = use_case.execute(request=request)

        return response.items
