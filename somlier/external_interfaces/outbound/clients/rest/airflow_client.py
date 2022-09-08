from typing import Any, Dict, List, Optional

import requests
from loguru import logger
from pydantic import validate_arguments
from requests.exceptions import ConnectTimeout, RetryError

from somlier.application.ports.clients.airflow_client import (
    AirflowClient,
    AirflowClientError,
)
from somlier.external_interfaces.exceptions import (
    ConnectionTimeoutError,
    HealthcheckError,
)


class AirflowRESTClient(AirflowClient):
    @validate_arguments(config={"arbitrary_types_allowed": True})
    def __init__(
        self, host: str, headers: Dict[str, str], timeout: int, session: Optional[requests.Session] = None
    ) -> None:
        self.host = host
        self.headers = headers
        self.timeout = timeout
        self.session = session or requests.Session()
        self._logger = logger

    def find_dag(self, dag_id: str) -> str:
        self.healthcheck()

        try:
            return self._find_dag(dag_id=dag_id)
        except RetryError as exc:
            error_message = f"[{dag_id}]를 찾을 수 없습니다"
            self._logger.error(error_message)
            raise exc

    def list_dags(self) -> List[Dict[str, Any]]:
        self.healthcheck()

        # 반환 값 구조는 아래 링크를 참고하세요.
        # ref: https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/get_dags
        response = self.session.get(
            f"{self.host}/api/v1/dags",
            headers=self.headers,
            timeout=self.timeout,
        )
        if not response.ok:
            raise AirflowClientError(title="에어플로우 클라이언트에서 에러가 발생했습니다.", detail=response.json())
        data = response.json()
        return data["dags"]

    def healthcheck(self) -> None:
        try:
            response = self.session.get(f"{self.host}/health", headers=self.headers, timeout=self.timeout)
        except ConnectTimeout as e:
            raise ConnectionTimeoutError(title="Airflow에 연결할 수 없습니다. VPN이 켜져있나 확인해주세요.", detail=str(e))
        if not response.ok:
            raise HealthcheckError(title="Airflow 헬스체크에 실패했습니다.")

    def _find_dag(self, dag_id: str) -> str:
        self.session.get(
            f"{self.host}/api/v1/dags/{dag_id}",
            headers=self.headers,
            timeout=self.timeout,
        )

        self._logger.info(f"[{dag_id}]를 찾았습니다")
        return f"{self.host}/tree?dag_id={dag_id}"
