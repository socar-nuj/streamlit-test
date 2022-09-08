import ast
import itertools
from typing import List, Dict

import numpy as np
from loguru import logger

from somlier.application.ports.clients.mlflow_client import MLflowClient
from somlier.application.use_cases.online.train.exceptions import (
    ParamsTypeCastError,
    InvalidContinuousParamError,
    EmptyParamsError,
)
from somlier.application.use_cases.online.train.request import TrainRequest
from somlier.application.use_cases.online.train.response import TrainResponse


def is_real_number(string: str) -> bool:
    try:
        int(string) or float(string)
    except ValueError:
        return False
    return True


class Train:
    def __init__(self, mlflow_client: MLflowClient, default_project_uri: str) -> None:
        self.mlflow_client = mlflow_client
        self.default_project_uri = default_project_uri
        self._logger = logger

    def execute(self, request: TrainRequest) -> List[TrainResponse]:
        if not request.project_uri:
            request.project_uri = self.default_project_uri
        project_uri_with_project_name = f"{request.project_uri}#{request.project_name}"

        self.mlflow_client.check_if_project_exists(
            uri=project_uri_with_project_name,
            version=request.project_ref,
            entrypoint=request.project_entrypoint,
        )

        params_combination = self._parse_params_and_generate_combination(request.params)
        train_responses = []
        use_synchronous = len(params_combination) == 1

        # 각 조합마다 MLflow run을 제출한다. 내부적으로는 async하게 실행된다.
        for param in params_combination:
            logger.info(f"Submit run for parameter {param}...")
            submitted_run = self.mlflow_client.submit_run(
                uri=project_uri_with_project_name,
                version=request.project_ref,
                entrypoint=request.project_entrypoint,
                parameters=param,
                experiment_name=request.project_name,
                use_k8s_job=request.use_k8s_job,
                use_gpu=request.use_gpu,
                synchronous=use_synchronous,
            )
            train_responses.append(TrainResponse(run_id=submitted_run.run_id, status=submitted_run.get_status()))

        return train_responses

    def _parse_params_and_generate_combination(self, params: Dict) -> List[Dict]:
        if not params:
            return [{}]

        parsed_params = dict()
        for param_name, param_values in params.items():
            parsed_values = self._validate_and_parse_param_values(param_values)
            parsed_params[param_name] = parsed_values

            if len(parsed_params[param_name]) <= 0:
                raise EmptyParamsError(title=f"조건에 일치하는 파라미터가 없습니다. [{param_name}]")

        name, values = zip(*parsed_params.items())
        params_combination = [dict(zip(name, v)) for v in itertools.product(*values)]

        return params_combination

    def _validate_and_parse_param_values(self, param_values: str) -> np.array:
        # case 1. 연속형 파라미터가 start..end..increment 형식으로 들어올 때
        if ".." in param_values:
            try:
                start, end, increment = [ast.literal_eval(pv) for pv in param_values.split("..")]
            except ValueError as e:
                raise ParamsTypeCastError(title="잘못된 파라미터 타입입니다.", detail=str(e.args))

            if (increment > 0 and start > end) or (increment < 0 and start < end):
                raise InvalidContinuousParamError(title="잘못된 연속형 파라미터 값입니다.", detail=f"{start:}, {end:}, {increment:}")
            parsed_values = np.arange(
                start, end, increment
            )  # TODO: 연속형 파라미터가 배수로 들어올 수도 있을 것 (ex. learning rate = 1e-4, 1e-5, 1e-6)

        # case 2. 불연속형 파라미터가 들어올 때
        elif "," in param_values:
            try:
                parsed_values = np.asarray(
                    [ast.literal_eval(pv) if is_real_number(pv) else pv for pv in param_values.split(",")]
                )
            except ValueError as e:
                raise ParamsTypeCastError(title="잘못된 파라미터 타입입니다.", detail=str(e.args))

        # case 3. 값을 하나만 가지는 파라미터가 들어올 때
        else:
            try:
                parsed_values = np.asarray(
                    ast.literal_eval(param_values) if is_real_number(param_values) else param_values
                ).reshape(-1)
            except ValueError as e:
                raise ParamsTypeCastError(title="잘못된 파라미터 타입입니다.", detail=str(e.args))

        return parsed_values
