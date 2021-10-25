from typing import Optional

from fastapi import APIRouter, Depends

from app.common.utils import propagate_args
from app.models.schemas.reviews import ReviewSuggestions
from app.models.schemas.suggestions import SuggestionsForApprove
from app.models.schemas.users import User
from app.common.deps import get_current_user, get_current_admin_user, pagination
from app.services.suggestions import SuggestionService

router = APIRouter()


@router.get('', response_model=SuggestionsForApprove, response_model_exclude_unset=True)
async def get_suggestions(
        common_args: dict = Depends(pagination),
        service: SuggestionService = Depends(),
        user: User = Depends(get_current_admin_user),
):
    data, total = await service.get_all_suggestions(user, common_args)
    resp = {'data': data,
            'total': total}
    propagate_args(common_args, resp)
    return resp


@router.post('/submit')
async def submit_review_suggestions(
        suggestions: ReviewSuggestions,
        service: SuggestionService = Depends(),
        user: User = Depends(get_current_user),
        changes: Optional[bool] = True,
):
    status = await service.submit_suggestions(suggestions, user, changes)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.delete('/{suggestions_id}/delete')
async def delete_suggestions(
        suggestions_id: int,
        service: SuggestionService = Depends(),
        user: User = Depends(get_current_user),
):
    status = await service.delete_suggestion(suggestions_id, user)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.get('/{suggestions_id}/approve')
async def approve_review_suggestions(
        suggestions_id: int,
        service: SuggestionService = Depends(),
        user: User = Depends(get_current_admin_user),
):
    status = await service.approve_suggestions(suggestions_id)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.post('/{suggestions_id}/reject')
async def reject_review_suggestions(
        suggestions_id: int,
        service: SuggestionService = Depends(),
        user: User = Depends(get_current_user),
):
    status = await service.reject_suggestions(suggestions_id)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}
