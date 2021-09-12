from fastapi import Depends
from sqlalchemy import delete
from sqlalchemy.orm import Session

from app.core.db import get_db, database
from app.models.domain.tables import reviews_suggestions
from app.repositories.base import BaseRepository


class SuggestionRepository(BaseRepository):

    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    @staticmethod
    async def delete_suggestion(suggestions_id, user):
        stmt = delete(reviews_suggestions).where(
            reviews_suggestions.c.reviews_suggestions_id == suggestions_id).where(
            reviews_suggestions.c.users_id == user.users_id)
        # self.session.execute(stmt)
        await database.execute(stmt)
