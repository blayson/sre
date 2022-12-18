from datetime import datetime, timedelta

from asyncpg import Record
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt

from app.models.schemas.auth import Token
from app.models.schemas.users import User, UserInRegister
from app.services.users import UsersService
from app.settings import settings
from app.utils.db import database
from app.utils.error_handlers import forbidden_error, unauthorized_error

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/routes/v1/auth/login")


class AuthService:
    def __init__(self, users_service: UsersService = Depends()):
        self.users_service: UsersService = users_service

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    async def verify_token(self, token: str) -> User:
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise unauthorized_error from None

        user_email = payload.get("user").get("email")
        user: Record = await self.users_service.get_user_by_email(user_email)
        return User.parse_obj(user)

    @classmethod
    def create_token(cls, user: Record) -> Token:
        user_data = User.parse_obj(user)
        now = datetime.utcnow()
        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(seconds=settings.jwt_expires_s),
            "sub": str(user_data.users_id),
            "user": user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
        )
        return Token(token=token)

    async def register_new_user(self, user_data: UserInRegister) -> Token:
        async with database.transaction():
            user = await self.users_service.create_user(user_data)
            return self.create_token(user)

    async def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> Token:
        user = await self.users_service.get_user_by_email(email)

        if not user:
            raise forbidden_error

        if not self.verify_password(password, user["password"]):
            raise forbidden_error

        return self.create_token(user)

    async def change_password(self, email: str, password: str):
        pass
