from datetime import datetime
from typing import List

from passlib.handlers.bcrypt import bcrypt
from pydantic import validator

from app.models.schemas.base import BaseSchemaORM
from app.models.validators import not_empty, normalize


class BaseUserORM(BaseSchemaORM):
    name: str
    email: str
    register_language: int = 2
    user_roles_id: int = 1


class User(BaseUserORM):
    users_id: int


class UserList(BaseSchemaORM):
    __root__: List[User]


class UserInRegister(BaseUserORM):
    password: str
    registered: datetime = None

    _not_empty = validator('name', 'email', allow_reuse=True, pre=True, always=True)(not_empty)
    _normalize_name = validator('name', allow_reuse=True)(normalize)

    @validator("name", pre=True, always=True)
    def length_name(cls, v: str):
        if len(v) > 64:
            raise ValueError('must be less then 64 symbols')
        return v

    @validator("password", pre=True, always=True)
    def hash_password(cls, v: str):  # noqa: N805, WPS110
        if len(v) < 5:
            raise ValueError('minimum 5 characters required')
        return bcrypt.hash(v)

    @validator("registered", pre=True, always=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.utcnow()
