from typing import List

from asyncpg import Record, UniqueViolationError
from fastapi import HTTPException
from pydantic import ValidationError
from starlette import status

from app.core.db import database
from app.core.exceptions import internal_server_error
from app.models.domain.tables import TUsers
from app.models.schemas.users import User, UserInRegister


class UsersService:

    @classmethod
    async def get_user_by_email(cls, email: str) -> Record:
        query = TUsers.select().where(email == TUsers.c.email)
        user_data: Record = await database.fetch_one(query)
        # user = User.parse_obj(user_data)
        return user_data

    @classmethod
    async def get_user_by_id(cls, user_id: str) -> Record:
        query = TUsers.select().where(user_id == TUsers.c.user_id)
        user_data: Record = await database.fetch_one(query)
        # user = User.parse_obj(user_data)
        return user_data

    @classmethod
    async def get_all_users(cls) -> List[User]:
        query = TUsers.select()
        user_data = await database.fetch_all(query)
        return [User.parse_obj(row) for row in user_data]

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
