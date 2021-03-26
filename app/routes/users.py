from typing import List

from fastapi import APIRouter, Depends

from app.models.schemas.users import User
from app.services.auth import get_current_user
from app.services.users import UsersService

router = APIRouter()


@router.get('/user', response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user


@router.get('/list', response_model=List[User], dependencies=[Depends(get_current_user)])
async def get_user():
    return await UsersService.get_all_users()
