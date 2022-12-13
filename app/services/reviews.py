from typing import List, Mapping, Optional, Tuple

from fastapi import Depends

from app.models.schemas.reviews import (
    ProductCategory,
    ReviewSuggestions,
    ReviewTable,
    SuggestionFeature,
    SuggestionSentiment,
)
from app.models.schemas.users import User
from app.repositories.reviews import ReviewsRepository
from app.services.base import BaseService
from app.utils.constants import UserReviewState


class ReviewService(BaseService):
    def __init__(self, repository: ReviewsRepository = Depends()):
        self.repository: ReviewsRepository = repository

    async def get_review_by_id(self, review_id: int) -> Optional[Mapping]:
        return await self.repository.get_review_by_id(review_id)

    async def get_review_list(
        self, common_args: dict, user: User
    ) -> Tuple[List[ReviewTable], int]:
        rows = await self.repository.get_reviews(common_args, user)
        feature_names = await self.repository.preload_feature_names()
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
        return await self.repository.get_product_categories()

    def get_review_suggestions(self, review_id):
        pass

    def get_update_by_id(self, review_id):
        pass
