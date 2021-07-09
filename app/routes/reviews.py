from fastapi import APIRouter, Depends

from app.models.schemas.reviews import ReviewList, Review
from app.services.reviews import ReviewService

router = APIRouter()


@router.get('/{review_id}', response_model=Review)
async def get_review(
        review_id: int,
        service: ReviewService = Depends()
) -> Review:
    return Review.parse_obj(service.get_review_by_id(review_id))


@router.get('/list', response_model=ReviewList)
async def get_review_list(
        page: int = 0,
        size: int = 10,
        service: ReviewService = Depends()
) -> ReviewList:
    return ReviewList.parse_obj(await service.get_review_list(page, size))