import logging
from typing import Optional

from fastapi import APIRouter, Depends

from app.models.schemas.reviews import ReviewSuggestions
from app.models.schemas.users import User
from app.services.suggestions import SuggestionService
from app.utils.deps import get_current_user

router = APIRouter()
logger = logging.getLogger("sre_api")


@router.post("/submit")
async def submit_review_suggestions(
    suggestions: ReviewSuggestions,
    service: SuggestionService = Depends(),
    user: User = Depends(get_current_user),
    changes: Optional[bool] = True,
):
    reviews_id = await service.submit_suggestions(suggestions, user, changes)
    if reviews_id:
        return {"status": "Ok"}
    else:
        return {"status": "error"}


@router.delete("/{suggestions_id}/delete")
async def delete_suggestions(
    suggestions_id: int,
    service: SuggestionService = Depends(),
    user: User = Depends(get_current_user),
):
    reviews_id = await service.delete_suggestion(suggestions_id, user)
    if reviews_id:
        return {"status": "Ok"}
    else:
        return {"status": "error"}
