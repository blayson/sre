from databases.backends.postgres import Record
from sqlalchemy import func

from app.core.db import database
from app.models.domain.tables import TReviews
from app.models.schemas.reviews import ReviewList, ReviewPage
from app.services.base import BaseService


class ReviewService(BaseService):

    @staticmethod
    async def get_review_by_id(review_id: int) -> Record:
        query = TReviews.select().where(review_id == TReviews.c.review_id)
        return await database.fetch_one(query)

    async def get_review_list(self, page: int, size: int) -> ReviewPage:
        total_query = TReviews.select(func.count())
        total = database.fetch_one(total_query)
        query = TReviews.select()
        query = self.paginate(query, page, size)
        rows: Record = await database.fetch_all(query=query)
        review_list = ReviewList.parse_obj(rows)
        return ReviewPage(data=review_list, page=page, size=size, total=total)
