from passlib.handlers.bcrypt import bcrypt
from pydantic import validator

from app.models.schemas.base import BaseSchema, BaseSchemaORM


class Token(BaseSchemaORM):
    token: str


class ChangedPasswordIn(BaseSchema):
    password: str

    @validator("password", pre=True, always=True)
    def hash_password(cls, v: str):  # noqa: N805, WPS110
        if len(v) < 5:
            raise ValueError("minimum 5 characters required")
        return bcrypt.hash(v)
