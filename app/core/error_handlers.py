from typing import Union

from fastapi import HTTPException, status
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

internal_server_error = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail='Internal server error',
)

forbidden_error = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail='Incorrect email or password',
)

unauthorized_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='',
)

conflict_error = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail='User already exist',
)


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        {"detail": exc.detail},
        status_code=exc.status_code,
        headers={'WWW-Authenticate': 'Bearer'},
    )


async def http422_error_handler(_: Request, exc: Union[RequestValidationError, ValidationError]) -> JSONResponse:
    return JSONResponse(
        {"detail": exc.errors()},
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )
