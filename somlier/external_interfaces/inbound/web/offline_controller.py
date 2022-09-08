import os

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from somlier.application.use_cases.offline.create import CreateBatch, CreateBatchRequest
from somlier.application.use_cases.offline.list import ListBatches, ListBatchesRequest
from somlier.external_interfaces.container import AppContainer

offline_router = APIRouter(prefix="/offline")


@offline_router.post("/create")
@inject
def create(
    request: CreateBatchRequest, use_case: CreateBatch = Depends(Provide[AppContainer.offline_container.create])
):
    response = use_case.execute(request=request)

    dag_path = f"./{request.dag_id}.py"
    with open(dag_path, "w") as file:
        file.write(response.dag)
    return FileResponse(
        path=dag_path, filename=f"{request.dag_id}.py", background=BackgroundTask(lambda: os.unlink(dag_path))
    )


@offline_router.get("/list")
@inject
def list_(request: ListBatchesRequest, use_case: ListBatches = Depends(Provide[AppContainer.offline_container.list])):
    response = use_case.execute(request=request)
    return response
