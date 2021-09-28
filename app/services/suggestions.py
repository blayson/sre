from fastapi import Depends

from app.models.schemas.reviews import ReviewSuggestions
from app.models.schemas.suggestions import SuggestionForApprove
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

    async def get_all_suggestions(self, user: User, common_args: dict):
        result = []
        if common_args['status'] == 'forApprove':
            async for row in await self.repository.get_all_suggestions(user, common_args):
                suggestion = SuggestionForApprove(**{
                    'reviews_suggestions_id': row[0],
                    'users_id': row[1],
                    'suggestion_time': row[2],
                    'reviews_id': row[3],
                    'changes': {
                        'sentiment': {
                            'old_value': row[7],
                            'new_value': row[4]
                        },
                        'feature': {
                            'old_value': row[9],
                            'new_value': row[6]
                        }
                    },
                    'state': row[10]
                })
                result.append(suggestion)

        return result

    def approve_suggestions(self, suggestions_id):
        pass

    def reject_suggestions(self, suggestions_id):
        pass
