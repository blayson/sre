from fastapi import APIRouter, Depends

from app.models.schemas.users import User
from app.services.auth import get_current_user
from app.services.suggestions import SuggestionService

router = APIRouter()


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


@router.post('/suggestions')
async def get_suggestions(
        service: SuggestionService = Depends()
):
    status = await service.get_all_suggestions()
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}
