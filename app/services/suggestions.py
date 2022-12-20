import logging

from fastapi import Depends
from sqlalchemy.exc import DatabaseError

from app.models.schemas.reviews import ReviewSuggestions
from app.models.schemas.users import User
from app.repositories.suggestions import (
    SuggestionRepository,
)
from app.services.base import BaseService
from app.utils.error_handlers import internal_server_error

logger = logging.getLogger("sre_api")


class SuggestionService(BaseService):
    def __init__(self, repository: SuggestionRepository = Depends()):
        self.repository: SuggestionRepository = repository

    async def submit_suggestions(
        self, suggestions: ReviewSuggestions, user: User, changes: bool
    ):
        try:
            if changes:
                status = await self.repository.submit_suggestions(suggestions, user)
            else:
                status = await self.repository.submit_no_suggestions(suggestions, user)
            return status
        except DatabaseError as exc:
            logger.exception("Exception during submitting suggestion %s", suggestions)
            raise internal_server_error from exc

    async def delete_suggestion(self, suggestions_id: int, user: User):
        try:
            return await self.repository.delete_suggestion(suggestions_id, user)
        except DatabaseError as exc:
            logger.exception("Exception during deleting suggestion %s", suggestions_id)
            raise internal_server_error from exc

    async def edit_suggestions(self, suggestions_id: int, corrections: ReviewSuggestions):
        try:
            return await self.repository.edit_suggestion(suggestions_id, corrections)
        except DatabaseError as exc:
            logger.exception("Exception during editing suggestion %s", suggestions_id)
            raise internal_server_error from exc
