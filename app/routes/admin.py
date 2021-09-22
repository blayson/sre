from fastapi import APIRouter, Depends

from app.models.schemas.users import User, UserList
from app.core.deps import get_current_user
from app.services.users import UsersService

router = APIRouter()


@router.get('/user/{user_id}', response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user


@router.get('/users/list', response_model=UserList, dependencies=[Depends(get_current_user)])
async def get_user_list():
    return await UsersService.get_all_users()
