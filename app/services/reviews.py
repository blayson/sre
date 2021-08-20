from typing import Tuple, Optional, Mapping, List

from fastapi import Depends
from app.models.schemas.reviews import ReviewTable
from app.repositories.reviews import ReviewsRepository
from app.services.base import BaseService


class ReviewService(BaseService):

    def __init__(self, repository: ReviewsRepository = Depends()):
        self.repository: ReviewsRepository = repository

    async def get_review_by_id(self, review_id: int) -> Optional[Mapping]:
        return await self.repository.get_review_by_id(review_id)

    async def get_review_list(self, common_args: dict) -> Tuple[List[ReviewTable], int]:
        rows = await self.repository.get_reviews(common_args)
        try:
            total = rows[0].get('total_items')
            r_list = [ReviewTable(**row) for row in rows]
            return r_list, total
        except IndexError as exc:
            raise "No items" from exc  # TODO: log and handle properly
