import logging

from fastapi import Depends
from sqlalchemy.exc import DatabaseError

from app.models.schemas.suggestions import SuggestionForApprove
from app.models.schemas.users import User, UserDataToUpdate, UserList
from app.repositories.admin import AdminRepository
from app.repositories.base import ReviewsSuggestionsStatesEnum
from app.services.base import BaseService
from app.utils.error_handlers import internal_server_error

logger = logging.getLogger("sre_api")


class AdminService(BaseService):
    def __init__(self, repository: AdminRepository = Depends()):
        self.repository: AdminRepository = repository

    async def get_user_by_id(self, user_id: int) -> User:
        return User(**await self.repository.get_user_by_id(user_id))

    async def get_all_users(self, user: User) -> UserList:
        return UserList(data=await self.repository.get_all_users(user))

    async def approve_suggestion(self, suggestions_id: int):
        return await self.repository.approve_suggestion(suggestions_id)

    async def reject_suggestion(self, suggestions_id: int):
        return await self.repository.reject_suggestion(suggestions_id)

    async def get_all_suggestions(self, user: User, common_args: dict):
        result = []
        total = 0
        if common_args["status"] == "forApprove":
            async for row in await self.repository.get_all_suggestions(
                user, common_args, ReviewsSuggestionsStatesEnum.PENDING.value
            ):
                total = row[11]
                suggestion = SuggestionForApprove(
                    **{
                        "reviews_suggestions_id": row[0],
                        "users_id": row[1],
                        "suggestion_time": row[2],
                        "reviews_id": row[3],
                        "text": row[12],
                        "changes": {
                            "sentiment": {"old_value": row[7], "new_value": row[4]},
                            "feature": {"old_value": row[9], "new_value": row[6]},
                        },
                        "state": row[10],
                    }
                )
                result.append(suggestion)

        return result, total

    async def update_user(
        self, user_id: int, user_data: UserDataToUpdate, current_user: User
    ):
        try:
            return await self.repository.update_user(user_id, user_data, current_user)
        except DatabaseError as exc:
            logger.exception("Exception during updating user %s", user_id)
            raise internal_server_error from exc

    async def delete_user(self, user_id: int):
        try:
            return await self.repository.delete_user(user_id)
        except DatabaseError as exc:
            logger.exception("Exception during deleting user %s", user_id)
            raise internal_server_error from exc
