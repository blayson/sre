from fastapi import APIRouter, Body, Depends
from app.models.schemas.users import UserInLogin, UserInRegister, Token
from app.services.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=Token, name="auth:login")
async def login(
        user_login: UserInLogin = Body(..., embaded=True, alias="user"),
        service: AuthService = Depends(),
) -> Token:
    return await service.authenticate_user(user_login.email, user_login.password)


@router.post("/register", response_model=Token, name="auth:register")
async def register(
        user_register: UserInRegister = Body(..., embaded=True, alias="user"),
        service: AuthService = Depends(),
) -> Token:
    return await service.register_new_user(user_register)
