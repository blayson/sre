from fastapi import APIRouter, HTTPException, Body, Depends
from fastapi_jwt_auth import AuthJWT

router = APIRouter()


@router.get('/user')
def user(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    current_user = authorize.get_jwt_subject()
    return {"user": current_user}
