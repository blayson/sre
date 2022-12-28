from fastapi import APIRouter, Depends

from app.models.schemas.auth import ChangedPasswordIn
from app.models.schemas.suggestions import SuggestionsForApprove
from app.models.schemas.users import User, UserDataToUpdate, UserList
from app.services.admin import AdminService
from app.utils.deps import get_current_admin_user, pagination
from app.utils.utils import propagate_args

router = APIRouter()


@router.get(
    "/user/{user_id}",
    response_model=User,
    dependencies=[Depends(get_current_admin_user)],
)
async def get_user(
    user_id: int,
    service: AdminService = Depends(),
):
    return await service.get_user_by_id(user_id)


@router.get("/users", response_model=UserList)
async def get_user_list(
    service: AdminService = Depends(), user: User = Depends(get_current_admin_user)
):
    return await service.get_all_users(user)


@router.delete(
    "/users/{user_id}/delete",
    dependencies=[Depends(get_current_admin_user)],
)
async def delete_user(
    user_id: int,
    service: AdminService = Depends(),
):
    uid = await service.delete_user(user_id)
    if uid:
        return {"status": "Ok"}
    else:
        return {"status": "error"}


@router.put(
    "/users/{user_id}/update",
    dependencies=[Depends(get_current_admin_user)],
)
async def update_user(
    user_id: int,
    user_data_to_update: UserDataToUpdate,
    service: AdminService = Depends(),
):
    uid = await service.update_user(user_id, user_data_to_update)
    if uid:
        return {"status": "Ok"}
    else:
        return {"status": "error"}


@router.put(
    "/suggestions/{suggestions_id}/approve",
)
async def approve_review_suggestions(
    suggestions_id: int,
    service: AdminService = Depends(),
    user: User = Depends(get_current_admin_user),
):
    sid = await service.approve_suggestion(suggestions_id, user)
    if sid:
        return {"status": "Ok"}
    else:
        return {"status": "error"}


@router.put(
    "/suggestions/{suggestions_id}/reject",
)
async def reject_review_suggestions(
    suggestions_id: int,
    service: AdminService = Depends(),
    user: User = Depends(get_current_admin_user),
):
    sid = await service.reject_suggestion(suggestions_id, user)
    if sid:
        return {"status": "Ok"}
    else:
        return {"status": "error"}


@router.get(
    "/suggestions",
    response_model=SuggestionsForApprove,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_current_admin_user)],
)
async def get_suggestions(
    common_args: dict = Depends(pagination),
    service: AdminService = Depends(),
    user: User = Depends(get_current_admin_user),
):
    data, total = await service.get_all_suggestions(user, common_args)
    resp = {"data": data, "total": total}
    propagate_args(common_args, resp)
    return resp


@router.put(
    "/users/{users_id}/changePassword",
    dependencies=[Depends(get_current_admin_user)],
)
async def change_user_password(
    users_id: int,
    changed_password: ChangedPasswordIn,
    service: AdminService = Depends(),
):
    uid = await service.change_user_password(users_id, changed_password)
    if uid:
        return {"status": "Ok"}
    else:
        return {"status": "error"}
