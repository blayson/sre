from databases.backends.postgres import Record

from app.core.db import database
from app.models.domain.tables import TReviews
from app.services.base import BaseService


class ReviewService(BaseService):

    @staticmethod
    async def get_review_by_id(review_id: int) -> Record:
        query = TReviews.select().where(review_id == TReviews.c.review_id)
        return await database.fetch_one(query)

    async def get_review_list(self, page: int, size: int) -> Record:
        query = TReviews.select()
        query = self.paginate(query, page, size)
        rows: Record = await database.fetch_all(query=query)
        return rows
