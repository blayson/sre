import logging

from fastapi import Depends
from sqlalchemy.exc import DatabaseError

from app.models.schemas.users import UserInRegister
from app.repositories.users import UsersRepository
from app.services.base import BaseService
from app.utils.error_handlers import internal_server_error

logger = logging.getLogger("sre_api")


class UsersService(BaseService):
    def __init__(self, repository: UsersRepository = Depends()):
        self.repository: UsersRepository = repository

    async def create_user(self, user_data: UserInRegister):
        try:
            return await self.repository.create_user(user_data)
        except DatabaseError as exc:
            logger.exception("Exception during creating user")
            raise internal_server_error from exc

    async def get_user_by_email(self, email: str):
        try:
            return await self.repository.get_user_by_email(email)
        except DatabaseError as exc:
            logger.exception("Exception during getting user %s", email)
            raise internal_server_error from exc
