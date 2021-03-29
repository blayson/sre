from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.routes.api import router
from app.core.db import database
from app.core.exceptions import http_error_handler, http422_error_handler
from app.settings import settings


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.project_name,
        debug=settings.debug,
        version=settings.version
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.on_event("startup")
    async def startup():
        await database.connect()

    @application.on_event("shutdown")
    async def shutdown():
        await database.disconnect()

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(router, prefix=settings.api_prefix)

    return application


app = create_application()
