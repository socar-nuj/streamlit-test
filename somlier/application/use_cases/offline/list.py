from typing import List

from pydantic import BaseModel

from somlier.application.ports.clients.airflow_client import AirflowClient


class ListBatchesRequest(BaseModel):
    pass


class ListBatchesResponse(BaseModel):
    items: List[str]


class ListBatches:
    def __init__(self, airflow_client: AirflowClient) -> None:
        self.airflow_client = airflow_client

    def execute(self, request: ListBatchesRequest) -> ListBatchesResponse:
        dags = self.airflow_client.list_dags()
        items = [dag["dag_id"] for dag in dags]

        return ListBatchesResponse(items=items)
