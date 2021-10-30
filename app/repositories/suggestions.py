import logging

from sqlalchemy import delete, select, insert, update
from sqlalchemy.sql.functions import now, func

from app.utils.db import database
from app.models.domain.tables import reviews_suggestions, reviews_suggestions_states, feature_names, reviews
from app.models.schemas.reviews import ReviewSuggestions
from app.models.schemas.users import User
from app.repositories.base import BaseRepository, ReviewsSuggestionsStatesEnum, ReviewsFinalStateEnum

logger = logging.getLogger("sre_api")


class SuggestionRepository(BaseRepository):

    @staticmethod
    async def delete_suggestion(suggestions_id: int, user: User):
        stmt = delete(reviews_suggestions).where(
            reviews_suggestions.c.reviews_suggestions_id == suggestions_id).where(
            reviews_suggestions.c.users_id == user.users_id)
        await database.execute(stmt)

    @staticmethod
    async def submit_suggestions(suggestions: ReviewSuggestions, user: User):
        to_update = {"users_id": user.users_id,
                     "suggestion_time": now(),
                     "reviews_id": suggestions.reviews_id,
                     "reviews_suggestions_states_id": ReviewsSuggestionsStatesEnum.PENDING.value}
        if suggestions.sentiment and suggestions.sentiment.new_value != suggestions.sentiment.old_value:
            to_update["sentiment"] = suggestions.sentiment.new_value

        if suggestions.feature and suggestions.feature.new_value != suggestions.feature.old_value:
            select_stmt = select([feature_names.c.feature_names_id]).select_from(feature_names).where(
                feature_names.c.text.ilike(suggestions.feature.new_value))
            feature_names_id = await database.fetch_one(select_stmt)
            to_update["feature_names_id"] = feature_names_id[0]
            # to_update["feature_names_id"] = suggestions.feature.new_value

        insert_stmt = insert(reviews_suggestions).values(**to_update).returning()

        # do_update_stmt = insert_stmt.on_conflict_do_update(
        #     constraint='reviews_id',
        #     set_=dict(
        #         users_id=user.users_id,
        #         suggestion_time=now(),
        #         sentiment=updates.sentiment.new_value,
        #         feature_names_id=updates.feature.new_value,
        #         reviews_suggestions_states_id=row[0].reviews_suggestions_states_id
        #     ))

        return await database.execute(insert_stmt)

    async def submit_no_suggestions(self, suggestions: ReviewSuggestions, user: User):
        stmt = update(reviews).where(
            reviews.c.reviews_id == suggestions.reviews_id
        ).values(reviews_final_state_id=ReviewsFinalStateEnum.CORRECT.value).returning(reviews.c.reviews_id)

        return await database.fetch_val(stmt)

    async def get_all_suggestions(self, user: User, common_args: dict, status: ReviewsSuggestionsStatesEnum):
        fn1 = feature_names.alias('fn1')
        fn2 = feature_names.alias('fn2')
        rss = reviews_suggestions_states.alias('rss')

        selectable = [reviews_suggestions.c.reviews_suggestions_id,
                      reviews_suggestions.c.users_id,
                      reviews_suggestions.c.suggestion_time,
                      reviews_suggestions.c.reviews_id,
                      reviews_suggestions.c.sentiment,
                      reviews_suggestions.c.feature_names_id,
                      fn2.c.text.label('feature'),
                      reviews.c.sentiment.label('old_sentiment'),
                      reviews.c.feature_names_id.label('old_feature_names_id'),
                      fn1.c.text.label('old_feature'),
                      rss.c.name.label('state'),
                      func.count().over().label('total_items'),
                      reviews.c.text]

        stmt = select(selectable).select_from(reviews_suggestions).join(
            reviews, reviews_suggestions.c.reviews_id == reviews.c.reviews_id, isouter=True).join(
            fn1, fn1.c.feature_names_id == reviews.c.feature_names_id, isouter=True).join(
            fn2, fn2.c.feature_names_id == reviews_suggestions.c.feature_names_id, isouter=True).join(
            rss, reviews_suggestions.c.reviews_suggestions_states_id == rss.c.reviews_suggestions_states_id
        )

        if common_args['start'] or common_args['end']:
            stmt = self.paginate(stmt, common_args['start'], common_args['end'], False)
        else:
            stmt = self.paginate(stmt, common_args['page'], common_args['size'], True)

        stmt = stmt.where(reviews_suggestions.c.reviews_suggestions_states_id == status)
        return database.iterate(stmt)

    async def approve_suggestion(self, suggestions_id: int):
        stmt = update(reviews_suggestions).where(reviews_suggestions.c.reviews_suggestions_id == suggestions_id).values(
            reviews_suggestions_states_id=ReviewsSuggestionsStatesEnum.APPROVED.value
        ).returning(reviews_suggestions.c.reviews_id)
        reviews_id = await database.fetch_val(stmt)

        stmt = update(reviews).where(reviews.c.reviews_id == reviews_id).values(
            reviews_final_state_id=ReviewsFinalStateEnum.CORRECTED.value)
        await database.execute(stmt)

        # select_stmt = select(
        #     [reviews_suggestions.c.sentiment,
        #      reviews_suggestions.c.feature_names_id]
        # ).select_from(reviews_suggestions).where(reviews_suggestions.c.reviews_suggestions_id == suggestions_id)
        # suggestion = await database.fetch_one(select_stmt)

        stmt = update(reviews_suggestions)
        stmt = stmt.where(reviews_suggestions.c.reviews_id == reviews_id)
        stmt = stmt.values(reviews_suggestions_states_id=ReviewsSuggestionsStatesEnum.REJECTED.value)
        await database.execute(stmt)
        return reviews_id

    async def reject_suggestion(self, suggestions_id: int):
        stmt = update(reviews_suggestions).where(reviews_suggestions.c.reviews_suggestions_id == suggestions_id).values(
            reviews_suggestions_states_id=ReviewsSuggestionsStatesEnum.REJECTED.value
        ).returning(reviews_suggestions.c.reviews_id)
        return await database.fetch_val(stmt)

