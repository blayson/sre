import logging
from typing import Optional

from fastapi import APIRouter, Depends, Response, status

from app.utils.utils import propagate_args
from app.models.schemas.reviews import ReviewSuggestions
from app.models.schemas.suggestions import SuggestionsForApprove
from app.models.schemas.users import User
from app.utils.deps import get_current_user, get_current_admin_user, pagination
from app.services.suggestions import SuggestionService

router = APIRouter()
logger = logging.getLogger("sre_api")


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
    reviews_id = await service.submit_suggestions(suggestions, user, changes)
    if reviews_id:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.delete('/{suggestions_id}/delete')
async def delete_suggestions(
        suggestions_id: int,
        service: SuggestionService = Depends(),
        user: User = Depends(get_current_user),
):
    reviews_id = await service.delete_suggestion(suggestions_id, user)
    if reviews_id:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.put('/{suggestions_id}/approve')
async def approve_review_suggestions(
        suggestions_id: int,
        response: Response,
        service: SuggestionService = Depends(),
        user: User = Depends(get_current_admin_user),
):
    await service.approve_suggestion(suggestions_id)


@router.put('/{suggestions_id}/reject')
async def reject_review_suggestions(
        suggestions_id: int,
        service: SuggestionService = Depends(),
        user: User = Depends(get_current_admin_user),
):
    await service.reject_suggestion(suggestions_id)
