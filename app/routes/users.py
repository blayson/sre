from fastapi import APIRouter, Depends

from app.models.schemas.users import User, UserList
from app.utils.deps import get_current_user
from app.services.users import UsersService

router = APIRouter()


@router.get('/user', response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user


@router.get('/', response_model=UserList, dependencies=[Depends(get_current_user)])
async def get_user_list(
        service: UsersService = Depends()
):
    return await service.get_all_users()


@router.get('/suggestions', dependencies=[Depends(get_current_user)])
async def get_user_list(
        service: UsersService = Depends()
):
    return await service.get_all_users()
