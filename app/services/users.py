from typing import List, Optional

from asyncpg import Record, UniqueViolationError
from databases import Database
from fastapi import Depends

from app.models.domain.tables import users
from app.models.schemas.users import User, UserInRegister
from app.services.base import BaseService
from app.utils.db import database, get_db
from app.utils.error_handlers import conflict_error, internal_server_error


class UsersService(BaseService):
    @classmethod
    async def get_user_by_email(cls, email: str) -> Record:
        query = users.select().where(email == users.c.email)
        return await database.fetch_one(query)

    @staticmethod
    async def get_user_by_id(user_id: str) -> Record:
        query = users.select().where(user_id == users.c.user_id)
        return await database.fetch_one(query)

    @staticmethod
    async def get_all_users() -> List[Record]:
        query = users.select()
        return await database.fetch_all(query)

    @staticmethod
    async def create_user(user_data: UserInRegister) -> Record:
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
        except UniqueViolationError as e:
            raise conflict_error
        except Exception as e:
            print(e)
            raise internal_server_error
        return user
