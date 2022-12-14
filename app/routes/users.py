from fastapi import APIRouter, Depends

from app.models.schemas.users import User
from app.utils.deps import get_current_user

router = APIRouter()


@router.get("/me", response_model=User)
async def get_user(user: User = Depends(get_current_user)):
    return user
