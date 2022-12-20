import logging
import typing

from databases.backends.postgres import Record
from sqlalchemy import func, select, update, delete, or_
from sqlalchemy.orm import Query

from app.models.domain.tables import (
    feature_names,
    reviews,
    reviews_suggestions,
    reviews_suggestions_states,
    users,
    user_roles,
)
from app.models.schemas.auth import ChangedPasswordIn
from app.models.schemas.users import User, UserDataToUpdate, UserWithRole
from app.repositories.base import (
    BaseRepository,
    ReviewsFinalStateEnum,
    ReviewsSuggestionsStatesEnum,
)
from app.utils.constants import USER_ROLES_MAP
from app.utils.db import database

logger = logging.getLogger("sre_api")


class AdminRepository(BaseRepository):
    @staticmethod
    async def get_all_users(user: User) -> typing.List[UserWithRole]:
        stmt = (
            select(
                [
                    users.c.users_id,
                    users.c.name,
                    users.c.email,
                    users.c.register_language,
                    user_roles.c.name.label("user_role"),
                ]
            )
            .select_from(users)
            .join(user_roles, user_roles.c.user_roles_id == users.c.user_roles_id)
            .where(users.c.users_id != user.users_id)
            .where(users.c.user_roles_id.in_((1, 2)))
        )
        return [UserWithRole(**row) for row in await database.fetch_all(stmt)]

    @staticmethod
    async def get_user_by_id(user_id: int) -> Record:
        query = users.select().where(user_id == users.c.user_id)
        return await database.fetch_one(query)

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
            users.c.name.label("user_name"),
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
            .join(users, users.c.users_id == reviews_suggestions.c.users_id)
        )

        stmt = self.apply_filters(common_args, stmt)

        stmt = stmt.where(reviews_suggestions.c.reviews_suggestions_states_id == status)
        stmt = stmt.where(
            or_(
                reviews_suggestions.c.admin_id == user.users_id,
                reviews_suggestions.c.admin_id.is_(None),
            )
        )
        return database.iterate(stmt)

    def apply_filters(
            self,
            common_args: dict,
            query: Query,
    ) -> Query:
        if common_args["start"] or common_args["end"]:
            stmt = self.paginate(query, common_args["start"], common_args["end"], False)
        else:
            stmt = self.paginate(query, common_args["page"], common_args["size"], True)

        return stmt

    @staticmethod
    async def approve_suggestion(suggestions_id: int, user: User):
        """Approve suggestion and update reviews table"""
        stmt = (
            update(reviews_suggestions)
            .where(reviews_suggestions.c.reviews_suggestions_id == suggestions_id)
            .values(
                reviews_suggestions_states_id=ReviewsSuggestionsStatesEnum.APPROVED.value,
                admin_id=user.users_id,
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
    async def reject_suggestion(suggestions_id: int, user: User):
        """Reject Suggestion"""
        stmt = (
            update(reviews_suggestions)
            .where(reviews_suggestions.c.reviews_suggestions_id == suggestions_id)
            .values(
                reviews_suggestions_states_id=ReviewsSuggestionsStatesEnum.REJECTED.value,
                admin_id=user.users_id,
            )
            .returning(reviews_suggestions.c.reviews_id)
        )
        return await database.fetch_val(stmt)

    @staticmethod
    async def update_user(user_id: int, user_data: UserDataToUpdate):
        stmt = update(users).where(users.c.users_id == user_id)

        if user_data.name:
            stmt = stmt.values(name=user_data.name)
        if user_data.email:
            stmt = stmt.values(email=user_data.email)
        if user_data.user_role:
            stmt = stmt.values(user_roles_id=USER_ROLES_MAP[user_data.user_role])

        stmt = stmt.returning(users.c.users_id)
        return await database.fetch_val(stmt)

    @staticmethod
    async def delete_user(user_id: int):
        secret_user_id = await database.fetch_val(
            select(users.c.users_id).where(users.c.user_roles_id == 4)
        )

        stmt = (
            update(reviews_suggestions)
            .where(user_id == reviews_suggestions.c.admin_id)
            .values(admin_id=secret_user_id)
        )
        await database.execute(stmt)

        stmt = (
            update(reviews_suggestions)
            .where(user_id == reviews_suggestions.c.users_id)
            .values(users_id=secret_user_id)
        )
        await database.execute(stmt)

        stmt = (
            delete(users).where(users.c.users_id == user_id).returning(users.c.users_id)
        )
        return await database.fetch_val(stmt)

    @staticmethod
    async def change_user_password(user_id: int, changed_password: ChangedPasswordIn):
        stmt = (
            update(users)
            .where(user_id == users.c.users_id)
            .values(password=changed_password.password)
            .returning(users.c.users_id)
        )
        return await database.fetch_val(stmt)
