from asyncpg import Record, UniqueViolationError

from app.utils.db import database
from app.utils.error_handlers import internal_server_error, conflict_error
from app.models.domain.tables import users
from app.models.schemas.users import UserInRegister
from app.services.base import BaseService


class UsersService(BaseService):
    @classmethod
    async def get_user_by_email(cls, email: str) -> Record:
        query = users.select().where(email == users.c.email)
        return await database.fetch_one(query)

    @classmethod
    async def get_user_by_id(cls, user_id: str) -> Record:
        query = users.select().where(user_id == users.c.user_id)
        return await database.fetch_one(query)

    @classmethod
    async def get_all_users(cls) -> Record:
        query = users.select()
        return await database.fetch_all(query)

    @classmethod
    async def create_user(cls, user_data: UserInRegister) -> Record:
        try:
            query = users.insert().returning(
                users.c.users_id,
                users.c.email,
                users.c.name,
                users.c.user_roles_id,
                users.c.register_language
            ).values(**user_data.dict())
            user: Record = await database.fetch_one(query)
        except UniqueViolationError as e:
            raise conflict_error
        except Exception as e:
            print(e)
            raise internal_server_error
        return user
