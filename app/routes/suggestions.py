from typing import Optional

from fastapi import APIRouter, Depends

from app.models.schemas.reviews import ReviewSuggestions
from app.models.schemas.users import User
from app.core.deps import get_current_user, get_current_admin_user
from app.services.suggestions import SuggestionService

router = APIRouter()


@router.post('')
async def get_suggestions(
        service: SuggestionService = Depends(),
        user: User = Depends(get_current_user),
):
    status = await service.get_all_suggestions()
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


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
