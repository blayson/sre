from datetime import datetime, timedelta

from asyncpg import Record, UniqueViolationError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError
from starlette import status

from app.core.exceptions import internal_server_error
from app.settings import settings
from app.models.schemas.users import User, Token, UserInRegister
from app.models.domain import tables
from app.core.db import database

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.verify_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def verify_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
        )
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: Record) -> Token:
        user_data = User.parse_obj(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_s),
            'sub': str(user_data.users_id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return Token(token=token)

    @database.transaction()
    async def register_new_user(self, user_data: UserInRegister) -> Token:
        try:
            query = tables.Users.insert().returning(
                tables.Users.c.users_id,
                tables.Users.c.email,
                tables.Users.c.name,
                tables.Users.c.user_roles_id,
                tables.Users.c.register_language
            ).values(**user_data.dict())
            user = await database.fetch_one(query)
        except UniqueViolationError as e:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User already exist',
            )
        except Exception as e:
            raise internal_server_error

        return self.create_token(user)

    async def authenticate_user(self, email: str, password: str, ) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
        )
        async with database.transaction():
            query = tables.Users.select().where(tables.Users.c.email == email)
            user = await database.fetch_one(query)

        if not user:
            raise exception

        if not self.verify_password(password, user['password']):
            raise exception

        return self.create_token(user)
