from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from starlette.responses import PlainTextResponse

from somlier.application.use_cases.online.cleanup import (
    Cleanup,
    CleanupRequest,
    CleanupResponse,
)
from somlier.application.use_cases.online.deploy import DeployRequest, DeployResponse
from somlier.application.use_cases.online.register.handler import Register
from somlier.application.use_cases.online.register.request import RegisterRequest
from somlier.application.use_cases.online.register.response import RegisterResponse
from somlier.application.use_cases.online.search import (
    Search,
    SearchRequest,
    SearchResponse,
)
from somlier.application.use_cases.online.train.handler import Train
from somlier.application.use_cases.online.train.request import TrainRequest
from somlier.application.use_cases.online.train.response import TrainResponse

from somlier.external_interfaces.container import AppContainer

online_router = APIRouter(prefix="/online")


@online_router.post("/train", response_model=TrainResponse)
@inject
def train(request: TrainRequest, use_case: Train = Depends(Provide[AppContainer.online_container.train])):
    """MLflow Project를 실행합니다."""

    response = use_case.execute(request)
    return response


@online_router.post("/search", response_model=SearchResponse)
@inject
def search(request: SearchRequest, use_case: Search = Depends(Provide[AppContainer.online_container.search])):
    """MLflow Project에서 standard_metric 값이 가장 낮은 실행을 출력합니다."""

    response = use_case.execute(request)
    return response


@online_router.post("/register", response_model=RegisterResponse)
@inject
def register(request: RegisterRequest, use_case: Register = Depends(Provide[AppContainer.online_container.register])):
    """MLflow 실행의 모델을 레지스트리에 등록합니다."""

    response = use_case.execute(request)
    return response


@online_router.post("/deploy", response_model=DeployResponse)
@inject
def deploy(request: DeployRequest, use_case_by_selector=Depends(Provide[AppContainer.online_container.deploy])):
    """MLflow Registry에 등록된 모델을 배포합니다."""

    if not request.use_k8s:
        raise HTTPException(status_code=HTTPStatus.NOT_IMPLEMENTED, detail="웹서버 모드에서는 준비중인 기능입니다")
    selector = "local" if request.use_k8s is False else "k8s"
    use_case = use_case_by_selector[selector]
    response = use_case.execute(request)
    return response


@online_router.post("/cleanup", response_model=CleanupResponse)
@inject
def cleanup(request: CleanupRequest, use_case: Cleanup = Depends(Provide[AppContainer.online_container.register])):
    response = use_case.execute(request)
    return response


@online_router.get("/health", response_class=PlainTextResponse)
def health():
    """서버 상태가 현재 정상인지 확인합니다."""

    return "I'm Alive!"
