from fastapi import Depends
from sqlalchemy import delete, select, insert
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import now

from app.core.db import get_db, database
from app.models.domain.tables import reviews_suggestions, reviews_suggestions_states, feature_names
from app.models.schemas.reviews import ReviewSuggestions
from app.models.schemas.users import User
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

    @staticmethod
    async def submit_suggestions(suggestions: ReviewSuggestions, user: User):
        selectable = [reviews_suggestions_states.c.reviews_suggestions_states_id]
        query_states = select(selectable).select_from(
            reviews_suggestions_states
        ).where(reviews_suggestions_states.c.name.ilike('pending'))

        row = await database.fetch_one(query_states)

        to_update = {"users_id": user.users_id,
                     "suggestion_time": now(),
                     "reviews_id": suggestions.reviews_id,
                     "reviews_suggestions_states_id": row[0]}
        if suggestions.sentiment:
            to_update["sentiment"] = suggestions.sentiment.new_value

        if suggestions.feature:
            select_stmt = select([feature_names.c.feature_names_id]).select_from(
                feature_names
            ).where(
                feature_names.c.text.ilike(suggestions.feature.new_value)
            )

            feature_names_id = await database.fetch_one(select_stmt)
            to_update["feature_names_id"] = feature_names_id[0]

        if suggestions.product:
            to_update["product"] = ""

        insert_stmt = insert(reviews_suggestions).values(**to_update)

        return await database.execute(insert_stmt)
        # do_update_stmt = insert_stmt.on_conflict_do_update(
        #     constraint='reviews_id ',
        #     set_=dict(
        #         users_id=user.users_id,
        #         suggestion_time=now(),
        #         sentiment=updates.sentiment.new_value,
        #         feature_names_id=updates.feature.new_value,
        #         reviews_suggestions_states_id=row[0].reviews_suggestions_states_id
        #     ))

    async def submit_no_suggestions(self, suggestions: ReviewSuggestions, user):
        pass
