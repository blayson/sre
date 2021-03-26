from asyncpg import Record, UniqueViolationError
from fastapi import HTTPException
from starlette import status

from app.core.db import database
from app.core.exceptions import internal_server_error
from app.models.domain.tables import TUsers
from app.models.schemas.users import UserInRegister


class UsersService:

    @classmethod
    async def get_user_by_email(cls, email: str) -> Record:
        query = TUsers.select().where(email == TUsers.c.email)
        return await database.fetch_one(query)

    @classmethod
    async def get_user_by_id(cls, user_id: str) -> Record:
        query = TUsers.select().where(user_id == TUsers.c.user_id)
        return await database.fetch_one(query)

    @classmethod
    async def get_all_users(cls) -> Record:
        query = TUsers.select()
        return await database.fetch_all(query)

    @classmethod
    async def create_user(cls, user_data: UserInRegister) -> Record:
        try:
            query = TUsers.insert().returning(
                TUsers.c.users_id,
                TUsers.c.email,
                TUsers.c.name,
                TUsers.c.user_roles_id,
                TUsers.c.register_language
            ).values(**user_data.dict())
            user: Record = await database.fetch_one(query)
        except UniqueViolationError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exist',
            )
        except Exception as e:
            raise internal_server_error
        return user
