from typing import Optional

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse, Response

from somlier.application.exceptions import (
    AlreadyExistError,
    ClientError,
    InvalidParameterError,
    NotFoundError,
)
from somlier.core.exceptions import Error


class ErrorJSONResponse(JSONResponse):
    def __init__(self, status_code: int, error: Error):
        super().__init__(
            status_code=status_code,
            content=jsonable_encoder({"status_code": status_code, **error.to_dict()}),
        )


def common_error_handler(request: Request, e: Error):
    if isinstance(e, InvalidParameterError):
        return ErrorJSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, error=e)

    if isinstance(e, NotFoundError):
        return ErrorJSONResponse(status_code=status.HTTP_404_NOT_FOUND, error=e)

    if isinstance(e, ClientError):
        return ErrorJSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=e)

    if isinstance(e, AlreadyExistError):
        return ErrorJSONResponse(status_code=status.HTTP_409_CONFLICT, error=e)

    if isinstance(e, NotImplementedError):
        return ErrorJSONResponse(status_code=status.HTTP_501_NOT_IMPLEMENTED, error=e)

    return ErrorJSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=e)


def python_error_handler(error: Exception) -> Optional[Response]:
    if isinstance(error, NotImplementedError):
        return JSONResponse(status_code=status.HTTP_501_NOT_IMPLEMENTED, content={"message": "아직 준비중인 기능입니다"})
    return None


async def exception_handler(request: Request, exc: Exception):
    if isinstance(exc, Error):
        return common_error_handler(request, exc)
    handled_error = python_error_handler(error=exc)
    if handled_error:
        return handled_error

    # TODO(humphrey): logging으로 핸들링 되지 않은 에러를 수집한다
    return exc
