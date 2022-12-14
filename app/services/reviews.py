import logging
from typing import List, Mapping, Optional, Tuple

import sqlalchemy.exc
from fastapi import Depends

from app.models.schemas.reviews import (
    ReviewTable,
    SuggestionFeature,
    SuggestionSentiment,
)
from app.models.schemas.users import User
from app.repositories.reviews import ReviewsRepository
from app.services.base import BaseService
from app.utils.constants import UserReviewState
from app.utils.error_handlers import internal_server_error


logger = logging.getLogger("sre_api")


class ReviewService(BaseService):
    def __init__(self, repository: ReviewsRepository = Depends()):
        self.repository: ReviewsRepository = repository

    async def get_review_by_id(self, review_id: int) -> Optional[Mapping]:
        try:
            return await self.repository.get_review_by_id(review_id)
        except sqlalchemy.exc.DatabaseError as exc:
            logger.exception("Exception during getting reviews")
            raise internal_server_error from exc

    async def get_review_list(
        self, common_args: dict, user: User
    ) -> Tuple[List[ReviewTable], int]:
        try:
            rows = await self.repository.get_reviews(common_args, user)
            feature_names = await self.repository.preload_feature_names()
        except sqlalchemy.exc.DatabaseError as exc:
            logger.exception("Exception during getting reviews")
            raise internal_server_error from exc

        try:
            total = rows[0].total_items
            r_list = []
            for row in rows:
                review_table = ReviewTable(**row)
                if (
                    common_args["status"]
                    and common_args["status"] == UserReviewState.REVIEWED.value
                ):
                    new_feature_name = None
                    if (
                        suggestion_feature_name_id := review_table.suggestion_feature_name
                    ):
                        new_feature_name = feature_names[
                            suggestion_feature_name_id
                        ].text
                    review_table.suggestion_feature_name = SuggestionFeature(
                        old=review_table.feature, new=new_feature_name
                    )
                    review_table.suggestion_sentiment = SuggestionSentiment(
                        old=review_table.sentiment,
                        new=review_table.suggestion_sentiment,
                    )
                r_list.append(review_table)

            return r_list, total
        except IndexError:
            return [], 0

    async def get_categories_list(self):
        try:
            return await self.repository.get_product_categories()
        except sqlalchemy.exc.DatabaseError as exc:
            logger.exception("Exception during getting categories")
            raise internal_server_error from exc
