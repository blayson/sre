from fastapi import Depends

from app.models.schemas.reviews import ReviewSuggestions
from app.models.schemas.users import User
from app.repositories.suggestions import SuggestionRepository
from app.services.base import BaseService


class SuggestionService(BaseService):

    def __init__(self, repository: SuggestionRepository = Depends()):
        self.repository: SuggestionRepository = repository

    async def delete_suggestion(self, suggestions_id: int, user: User):
        await self.repository.delete_suggestion(suggestions_id, user)

    async def submit_suggestions(self, suggestions: ReviewSuggestions, user: User, changes: bool):
        if changes:
            rows = await self.repository.submit_suggestions(suggestions, user)
        else:
            rows = await self.repository.submit_no_suggestions(suggestions, user)
        return rows

    def get_all_suggestions(self, user: User, commons: dict):
        pass

    def approve_suggestions(self, suggestions_id):
        pass

    def reject_suggestions(self, suggestions_id):
        pass
