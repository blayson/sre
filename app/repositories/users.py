import logging
from typing import Optional

from asyncpg import UniqueViolationError
from databases.backends.postgres import Record

from app.models.domain.tables import users
from app.models.schemas.users import UserInRegister
from app.repositories.base import BaseRepository
from app.utils.constants import USER_ROLES_MAP
from app.utils.db import database
from app.utils.error_handlers import conflict_error, internal_server_error

logger = logging.getLogger("sre_api")


class UsersRepository(BaseRepository):
    @staticmethod
    async def get_user_by_id(user_id: int) -> Record:
        query = users.select().where(user_id == users.c.user_id)
        return await database.fetch_one(query)

    @classmethod
    async def get_user_by_email(cls, email: str) -> Record:
        query = users.select().where(email == users.c.email)
        return await database.fetch_one(query)

    @staticmethod
    async def create_user(user_data: UserInRegister) -> Record:
        user_data.user_roles_id = USER_ROLES_MAP[user_data.user_role]
        del user_data.user_role
        try:
            query = (
                users.insert()
                .returning(
                    users.c.users_id,
                    users.c.email,
                    users.c.name,
                    users.c.user_roles_id,
                    users.c.register_language,
                )
                .values(**user_data.dict())
            )
            user: Optional[Record] = await database.fetch_one(query)
        except UniqueViolationError as exc:
            raise conflict_error from exc
        except Exception as exc:
            logger.exception("Internal server error")
            raise internal_server_error from exc
        return user
