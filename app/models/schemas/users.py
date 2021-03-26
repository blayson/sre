from pydantic import BaseModel, validator, EmailStr
from datetime import datetime, timezone
from passlib.hash import bcrypt


def normalize(name: str) -> str:
    return ' '.join((word.capitalize()) for word in name.split(' '))


def not_empty(val: str) -> str:
    assert val != '', 'Empty strings are not allowed'
    return val


def set_ts_now(val: datetime) -> datetime:
    return val or datetime.now(timezone.utc)


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


class BaseUser(BaseSchema):
    name: str
    email: str
    register_language: int = 2
    user_roles_id: int = 1


class User(BaseUser):
    users_id: int


class UserInRegister(BaseUser):
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


class UserWithToken(BaseUser):
    token: str


class Token(BaseSchema):
    token: str


class UserInResponse(BaseSchema):
    user: UserWithToken


class UserInLogin(BaseSchema):
    username: EmailStr
    password: str

    _not_empty = validator('username', allow_reuse=True)(not_empty)

    @validator("password", pre=True, always=True)
    def length(cls, v):
        if len(v) < 5:
            raise ValueError('minimum 5 characters required')
        return v
