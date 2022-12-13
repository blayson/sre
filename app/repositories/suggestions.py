import logging

from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Query
from sqlalchemy.sql.functions import func, now

from app.models.domain.tables import (
    feature_names,
    reviews,
    reviews_suggestions,
    reviews_suggestions_states,
)
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
        )
        await database.execute(stmt)

    @staticmethod
    async def submit_suggestions(suggestions: ReviewSuggestions, user: User):
        """Submit suggestions"""
        to_update = {
            "users_id": user.users_id,
            "suggestion_time": now(),
            "reviews_id": suggestions.reviews_id,
            "reviews_suggestions_states_id": ReviewsSuggestionsStatesEnum.PENDING.value,
        }

        stmt = (
            select([reviews.c.sentiment, feature_names.c.text])
            .select_from(reviews)
            .join(
                feature_names,
                reviews.c.feature_names_id == feature_names.c.feature_names_id,
            )
            .where(reviews.c.reviews_id == suggestions.reviews_id)
        )
        record = await database.fetch_one(stmt)
        initial_sentiment = record[0]
        initial_feature = record[1]

        if (
            suggestions.sentiment
            and suggestions.sentiment.new_value is not None
            and suggestions.sentiment.new_value != initial_sentiment
        ):
            to_update["sentiment"] = suggestions.sentiment.new_value

        if (
            suggestions.feature
            and suggestions.feature.new_value is not None
            and suggestions.feature.new_value != initial_feature
        ):
            select_stmt = (
                select([feature_names.c.feature_names_id])
                .select_from(feature_names)
                .where(feature_names.c.text.ilike(suggestions.feature.new_value))
            )
            feature_names_id = await database.fetch_val(select_stmt)
            to_update["feature_names_id"] = feature_names_id

        insert_stmt = insert(reviews_suggestions).values(**to_update).returning()
        return await database.execute(insert_stmt)

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

    async def get_all_suggestions(
        self, user: User, common_args: dict, status: ReviewsSuggestionsStatesEnum
    ):
        """Get all suggestions by status"""
        fn1 = feature_names.alias("fn1")
        fn2 = feature_names.alias("fn2")
        rss = reviews_suggestions_states.alias("rss")

        selectable = [
            reviews_suggestions.c.reviews_suggestions_id,
            reviews_suggestions.c.users_id,
            reviews_suggestions.c.suggestion_time,
            reviews_suggestions.c.reviews_id,
            reviews_suggestions.c.sentiment,
            reviews_suggestions.c.feature_names_id,
            fn2.c.text.label("feature"),
            reviews.c.sentiment.label("old_sentiment"),
            reviews.c.feature_names_id.label("old_feature_names_id"),
            fn1.c.text.label("old_feature"),
            rss.c.name.label("state"),
            func.count().over().label("total_items"),
            reviews.c.text,
        ]

        stmt = (
            select(selectable)
            .select_from(reviews_suggestions)
            .join(
                reviews,
                reviews_suggestions.c.reviews_id == reviews.c.reviews_id,
                isouter=True,
            )
            .join(
                fn1, fn1.c.feature_names_id == reviews.c.feature_names_id, isouter=True
            )
            .join(
                fn2,
                fn2.c.feature_names_id == reviews_suggestions.c.feature_names_id,
                isouter=True,
            )
            .join(
                rss,
                reviews_suggestions.c.reviews_suggestions_states_id
                == rss.c.reviews_suggestions_states_id,
            )
        )

        stmt = self.apply_filters(common_args, stmt)

        stmt = stmt.where(reviews_suggestions.c.reviews_suggestions_states_id == status)
        return database.iterate(stmt)

    def apply_filters(
        self,
        common_args: dict,
        query: Query,
        sortable: dict = None,
        filterable: dict = None,
        *args,
        **kwargs
    ) -> Query:
        if common_args["start"] or common_args["end"]:
            stmt = self.paginate(query, common_args["start"], common_args["end"], False)
        else:
            stmt = self.paginate(query, common_args["page"], common_args["size"], True)

        return stmt

    @staticmethod
    async def approve_suggestion(suggestions_id: int):
        """Approve suggestion and update reviews table"""
        stmt = (
            update(reviews_suggestions)
            .where(reviews_suggestions.c.reviews_suggestions_id == suggestions_id)
            .values(
                reviews_suggestions_states_id=ReviewsSuggestionsStatesEnum.APPROVED.value
            )
            .returning(
                reviews_suggestions.c.reviews_id,
                reviews_suggestions.c.sentiment,
                reviews_suggestions.c.feature_names_id,
            )
        )
        record = await database.fetch_one(stmt)
        reviews_id = record[0]
        sentiment = record[1]
        feature_names_id = record[2]

        stmt = (
            update(reviews)
            .where(reviews.c.reviews_id == reviews_id)
            .values(reviews_final_state_id=ReviewsFinalStateEnum.CORRECTED.value)
        )

        if sentiment is not None:
            stmt = stmt.values(sentiment=sentiment)
        if feature_names_id is not None:
            stmt = stmt.values(feature_names_id=feature_names_id)

        logger.debug(stmt)
        await database.execute(stmt)

        stmt = (
            update(reviews_suggestions)
            .where(
                (reviews_suggestions.c.reviews_id == reviews_id)
                & (reviews_suggestions.c.reviews_suggestions_id != suggestions_id)
            )
            .values(
                reviews_suggestions_states_id=ReviewsSuggestionsStatesEnum.REJECTED.value
            )
        )
        await database.execute(stmt)
        return reviews_id

    @staticmethod
    async def reject_suggestion(suggestions_id: int):
        """Reject Suggestion"""
        stmt = (
            update(reviews_suggestions)
            .where(reviews_suggestions.c.reviews_suggestions_id == suggestions_id)
            .values(
                reviews_suggestions_states_id=ReviewsSuggestionsStatesEnum.REJECTED.value
            )
            .returning(reviews_suggestions.c.reviews_id)
        )
        return await database.fetch_val(stmt)
