import typing

from asyncpg import Record
from sqlalchemy import func, select, types
from sqlalchemy.orm import Query
from sqlalchemy.sql import expression
from sqlalchemy.sql.functions import coalesce

from app.models.domain.tables import (
    feature_names,
    product_categories,
    products,
    reviews,
    reviews_suggestions,
    reviews_suggestions_states,
)
from app.models.schemas.features import FeatureTable
from app.models.schemas.users import User
from app.repositories.base import BaseRepository
from app.utils.constants import UserReviewState
from app.utils.db import database


class ReviewsRepository(BaseRepository):
    async def get_reviews(self, common_args: dict, user: User) -> typing.List[Record]:
        join = (
            reviews.join(
                products, products.c.products_id == reviews.c.products_id, isouter=True
            )
            .join(
                feature_names,
                feature_names.c.feature_names_id == reviews.c.feature_names_id,
                isouter=True,
            )
            .join(
                reviews_suggestions,
                reviews_suggestions.c.reviews_id == reviews.c.reviews_id,
                isouter=True,
            )
            .join(
                reviews_suggestions_states,
                reviews_suggestions_states.c.reviews_suggestions_states_id
                == reviews_suggestions.c.reviews_suggestions_states_id,
                isouter=True,
            )
        )

        selectable = [
            reviews.c.text,
            reviews.c.sentiment,
            products.c.name.label("product"),
            feature_names.c.text.label("feature"),
            reviews.c.published_at,
            coalesce(reviews_suggestions_states.c.name, None).label("status"),
            func.concat(
                expression.cast(reviews.c.reviews_id, types.Unicode),
                expression.cast("|", types.Unicode),
                expression.cast(feature_names.c.feature_names_id, types.Unicode),
            ).label("id"),
            func.count().over().label("total_items"),
        ]

        sortable = {
            "sentiment": reviews.c.sentiment,
            "product": products.c.name,
            "feature": feature_names.c.text,
            "date": reviews_suggestions.c.suggestion_time
            if common_args["status"] and common_args["status"] == "reviewed"
            else reviews.c.published_at,
        }

        filterable = {
            "product": products.c.name,
            "feature": feature_names.c.text,
            "text": reviews.c.text,
            "pcat": products.c.product_categories_id,
            "status": reviews_suggestions_states.c.name,
        }

        if (
            common_args["status"]
            and common_args["status"] == UserReviewState.REVIEWED.value
        ):
            selectable.append(
                reviews_suggestions.c.reviews_suggestions_id.label("suggestions_id")
            )
            selectable.append(reviews_suggestions.c.suggestion_time)
            selectable.append(
                reviews_suggestions.c.feature_names_id.label("suggestion_feature_name")
            ),
            selectable.append(
                reviews_suggestions.c.old_feature_names_id.label(
                    "old_suggestion_feature_name_id"
                )
            ),
            selectable.append(
                reviews_suggestions.c.sentiment.label("suggestion_sentiment")
            )
            selectable.append(
                reviews_suggestions.c.old_sentiment.label("old_suggestion_sentiment")
            )

        query = select(selectable).select_from(join)
        query = self._apply_filters(common_args, query, sortable, filterable, user=user)

        return await database.fetch_all(query)

    @staticmethod
    async def preload_feature_names() -> typing.Dict[str, FeatureTable]:
        feature_stmt = select(
            [feature_names.c.text, feature_names.c.feature_names_id]
        ).select_from(feature_names)
        features_q = await database.fetch_all(feature_stmt)
        return {
            feature["feature_names_id"]: FeatureTable(**feature)
            for feature in features_q
        }

    def _apply_filters(
        self,
        common_args: dict,
        query: Query,
        sortable: dict = None,
        filterable: dict = None,
        **kwargs
    ) -> Query:
        if common_args["start"] or common_args["end"]:
            query = self.paginate(
                query, common_args["start"], common_args["end"], False
            )
        else:
            query = self.paginate(query, common_args["page"], common_args["size"], True)

        if common_args["sort"]:
            query = self.apply_sort(query, common_args["sort"], sortable)
        else:
            query = self.apply_sort(query, "date desc", sortable)

        if common_args["product"]:
            query = self.filter(query, ("product", common_args["product"]), filterable)

        if common_args["feature"]:
            query = self.filter(query, ("feature", common_args["feature"]), filterable)

        if common_args["text"]:
            query = self.filter(query, ("text", common_args["text"]), filterable)

        if common_args["pcat"]:
            query = self.filter_by_pcategory(
                query, ("pcat", common_args["pcat"]), filterable
            )

        if common_args["status"]:
            user = kwargs["user"]
            query = self.filter_by_status(
                query, ("status", common_args["status"]), filterable, user
            )
        else:
            query = query.where(reviews_suggestions.c.reviews_id.is_(None))
        return query

    @staticmethod
    async def get_review_by_id(review_id: int) -> typing.Optional[typing.Mapping]:
        query = reviews.select().where(review_id == reviews.c.reviews_id)
        return await database.fetch_one(query)

    @staticmethod
    async def get_product_categories():
        query = select(
            [
                product_categories.c.product_categories_id.label("id"),
                product_categories.c.czech_name.label("product_category"),
            ]
        ).select_from(product_categories)
        return await database.fetch_all(query)
