from pydantic import BaseModel

from somlier.application.exceptions import NotFoundError
from somlier.application.ports.clients.mlflow_client import MLflowClient


class SearchRequest(BaseModel):
    project_name: str
    metric_by: str
    ascending: bool = False


class SearchResponse(BaseModel):
    run_id: str
    metric_value: str


class MLflowRunNotFoundError(NotFoundError):
    pass


class MLflowProjectNotFoundError(NotFoundError):
    pass


# class MLflowInvalidStandardMetricError(InvalidParameterError):
#     pass


class Search:
    def __init__(self, mlflow_client: MLflowClient) -> None:
        self.mlflow_client = mlflow_client

    def execute(self, request: SearchRequest) -> SearchResponse:
        experiment = self.mlflow_client.get_experiment_by_name(request.project_name)
        if not experiment:
            raise MLflowProjectNotFoundError(title="요청 내용 중 project_name 에 해당하는 프로젝트를 찾을 수 없습니다.")
        elif experiment.lifecycle_stage == "delete":
            raise MLflowProjectNotFoundError(title="요청 내용 중 project_name 에 해당하는 프로젝트는 이미 삭제된 프로젝트입니다.")

        runs = self.mlflow_client.find_runs_in_experiment_by_metric(
            experiment_id=experiment.experiment_id, metric=request.metric_by, ascending=request.ascending
        )

        if not runs:
            raise MLflowRunNotFoundError(title="요청에 해당하는 Run 이 없습니다.")
        run = runs[0]

        return SearchResponse(
            run_id=str(run.info.run_id),
            metric_value=str(run.data.metrics[request.metric_by]),
        )
