from typing import Tuple, Optional, Mapping, List

from fastapi import Depends
from app.models.schemas.reviews import ReviewTable, ProductCategory, ReviewSuggestions
from app.models.schemas.users import User
from app.repositories.reviews import ReviewsRepository
from app.services.base import BaseService


class ReviewService(BaseService):

    def __init__(self, repository: ReviewsRepository = Depends()):
        self.repository: ReviewsRepository = repository

    async def get_review_by_id(self, review_id: int) -> Optional[Mapping]:
        return await self.repository.get_review_by_id(review_id)

    async def get_review_list(self, common_args: dict, user: User) -> Tuple[List[ReviewTable], int]:
        rows = await self.repository.get_reviews(common_args, user)
        try:
            total = rows[0].get('total_items')
            # for row in rows:
            #     print(type(row.get('published_at')))
            r_list = [ReviewTable(**row) for row in rows]
            return r_list, total
        except IndexError as exc:
            return [], 0

    async def get_categories_list(self):
        return await self.repository.get_product_categories()

    def get_review_suggestions(self, review_id):
        pass

    def get_update_by_id(self, review_id):
        pass

