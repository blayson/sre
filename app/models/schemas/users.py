from datetime import datetime
from typing import List, Optional

from passlib.handlers.bcrypt import bcrypt
from pydantic import validator, root_validator

from app.models.schemas.base import BaseSchema, BaseSchemaORM
from app.models.validators import normalize, not_empty
from app.utils.constants import UserRoles


class BaseUserORM(BaseSchemaORM):
    name: str
    email: str
    register_language: Optional[int] = 1
    user_roles_id: Optional[int] = 1


class User(BaseUserORM):
    users_id: int


class UserWithRole(BaseSchemaORM):
    users_id: int
    name: str
    email: str
    register_language: Optional[int] = 1
    user_role: str


class UserList(BaseSchemaORM):
    data: List[UserWithRole]


class UserInRegister(BaseUserORM):
    password: str
    registered: datetime = None
    user_role: UserRoles = UserRoles.USER

    _not_empty = validator("name", "email", allow_reuse=True, pre=True, always=True)(
        not_empty
    )
    _normalize_name = validator("name", allow_reuse=True)(normalize)

    @validator("name", pre=True, always=True)
    def length_name(cls, v: str):
        if len(v) > 64:
            raise ValueError("must be less then 64 symbols")
        return v

    @validator("password", pre=True, always=True)
    def hash_password(cls, v: str):  # noqa: N805, WPS110
        if len(v) < 5:
            raise ValueError("minimum 5 characters required")
        return bcrypt.hash(v)

    @validator("registered", pre=True, always=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.utcnow()


class UserDataToUpdate(BaseSchema):
    name: Optional[str] = None
    email: Optional[str] = None
    user_role: Optional[UserRoles] = None

    @root_validator()
    def check_at_least_one(cls, values):
        if (
            values.get("name") is None
            and values.get("email") is None
            and values.get("user_role") is None
        ):
            raise ValueError("either name, email or user_roles_id is required")
        return values
