import logging

from sqlalchemy import delete, insert, select, update
from sqlalchemy.sql.functions import now

from app.models.domain.tables import feature_names, reviews, reviews_suggestions
from app.models.schemas.reviews import ReviewSuggestions
from app.models.schemas.users import User
from app.repositories.base import (
    BaseRepository,
    ReviewsFinalStateEnum,
    ReviewsSuggestionsStatesEnum,
)
from app.utils.db import database

logger = logging.getLogger("sre_api")


class SuggestionRepository(BaseRepository):
    @staticmethod
    async def delete_suggestion(suggestions_id: int, user: User):
        """Delete suggestions"""
        stmt = (
            delete(reviews_suggestions)
            .where(reviews_suggestions.c.reviews_suggestions_id == suggestions_id)
            .where(reviews_suggestions.c.users_id == user.users_id)
            .returning(reviews_suggestions.c.reviews_suggestions_id)
        )
        return await database.fetch_val(stmt)

    async def _prepare_suggestions(
        self, suggestions: ReviewSuggestions, to_update: dict
    ):
        (
            initial_sentiment,
            initial_feature_text,
            initial_feature_id,
        ) = await self._preload_initial_values(suggestions)
        if (
            suggestions.sentiment
            and suggestions.sentiment.new_value is not None
            and suggestions.sentiment.new_value != initial_sentiment
        ):
            to_update["sentiment"] = suggestions.sentiment.new_value
            to_update["old_sentiment"] = initial_sentiment

        if (
            suggestions.feature
            and suggestions.feature.new_value is not None
            and suggestions.feature.new_value != initial_feature_text
        ):
            select_stmt = (
                select([feature_names.c.feature_names_id])
                .select_from(feature_names)
                .where(feature_names.c.text.ilike(suggestions.feature.new_value))
            )
            feature_names_id = await database.fetch_val(select_stmt)
            to_update["feature_names_id"] = feature_names_id
            to_update["old_feature_names_id"] = initial_feature_id
        return to_update

    async def submit_suggestions(self, suggestions: ReviewSuggestions, user: User):
        """Submit suggestions"""
        to_update = {
            "users_id": user.users_id,
            "suggestion_time": now(),
            "reviews_id": suggestions.reviews_id,
            "reviews_suggestions_states_id": ReviewsSuggestionsStatesEnum.PENDING.value,
        }

        to_update = await self._prepare_suggestions(suggestions, to_update)
        if to_update.get("feature_names_id") or to_update.get("sentiment"):
            insert_stmt = (
                insert(reviews_suggestions)
                .values(**to_update)
                .returning(reviews_suggestions.c.reviews_suggestions_id)
            )
            return await database.fetch_val(insert_stmt)
        else:
            return None

    @staticmethod
    async def submit_no_suggestions(suggestions: ReviewSuggestions, user: User):
        """Submit without suggestions"""
        stmt = (
            update(reviews)
            .where(reviews.c.reviews_id == suggestions.reviews_id)
            .values(reviews_final_state_id=ReviewsFinalStateEnum.CORRECT.value)
            .returning(reviews.c.reviews_id)
        )

        return await database.fetch_val(stmt)

    async def edit_suggestion(
        self, suggestions_id: int, corrections: ReviewSuggestions
    ):
        (
            initial_sentiment,
            initial_feature_text,
            initial_feature_id,
        ) = await self._preload_initial_values(corrections)
        to_update = {}
        if corrections.sentiment and corrections.sentiment.new_value is not None:
            to_update["sentiment"] = corrections.sentiment.new_value
            to_update["old_sentiment"] = initial_sentiment

        if corrections.feature and corrections.feature.new_value is not None:
            select_stmt = (
                select([feature_names.c.feature_names_id])
                .select_from(feature_names)
                .where(feature_names.c.text.ilike(corrections.feature.new_value))
            )
            feature_names_id = await database.fetch_val(select_stmt)
            to_update["feature_names_id"] = feature_names_id
            to_update["old_feature_names_id"] = initial_feature_id

        if to_update.get("feature_names_id") or to_update.get("sentiment"):
            stmt = (
                update(reviews_suggestions)
                .where(reviews_suggestions.c.reviews_suggestions_id == suggestions_id)
                .values(**to_update)
                .returning(reviews_suggestions.c.reviews_suggestions_id)
            )
            return await database.fetch_val(stmt)
        else:
            return None

    @staticmethod
    async def _preload_initial_values(corrections: ReviewSuggestions):
        stmt = (
            select(
                [
                    reviews.c.sentiment,
                    feature_names.c.text,
                    feature_names.c.feature_names_id,
                ]
            )
            .select_from(reviews)
            .join(
                feature_names,
                reviews.c.feature_names_id == feature_names.c.feature_names_id,
            )
            .where(reviews.c.reviews_id == corrections.reviews_id)
        )
        record = await database.fetch_one(stmt)
        return record[0], record[1], record[2]
