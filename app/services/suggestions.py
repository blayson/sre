from fastapi import Depends

from app.models.schemas.users import User
from app.repositories.suggestions import SuggestionRepository
from app.services.base import BaseService


class SuggestionService(BaseService):

    def __init__(self, repository: SuggestionRepository = Depends()):
        self.repository: SuggestionRepository = repository

    async def delete_suggestion(self, suggestions_id: int, user: User):
        await self.repository.delete_suggestion(suggestions_id, user)

    def get_all_suggestions(self):
        pass
