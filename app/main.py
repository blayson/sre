import logging
from logging.config import dictConfig

from databases import Database
from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.routes.api import router
from app.settings import settings
from app.utils.db import database
from app.utils.error_handlers import http422_error_handler, http_error_handler

from .logger import LogConfig


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.project_name, debug=settings.debug, version=settings.version
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

    application.add_exception_handler(Exception, http_error_handler)
    # application.add_exception_handler(RequestValidationError, http422_error_handler)
    # application.add_exception_handler(ValidationError, http422_error_handler)

    application.include_router(router, prefix=settings.api_prefix)

    return application


# Setup logger
dictConfig(LogConfig().dict())
app = create_application()
