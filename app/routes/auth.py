from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.models.schemas.auth import Token
from app.models.schemas.users import UserInRegister
from app.services.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=Token, name="auth:login")
async def login(
        auth_data: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends(),
) -> Token:
    return await service.authenticate_user(auth_data.username, auth_data.password)


@router.post("/register", response_model=Token, name="auth:register", status_code=status.HTTP_201_CREATED)
async def register(
        user_register: UserInRegister,
        service: AuthService = Depends(),
) -> Token:
    return await service.register_new_user(user_register)
