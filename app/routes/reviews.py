from fastapi import APIRouter, Depends

from app.core.deps import pagination
from app.models.schemas.reviews import Review, ReviewPage
from app.services.reviews import ReviewService

router = APIRouter()


@router.get('/{review_id}', response_model=Review)
async def get_review(
        review_id: int,
        service: ReviewService = Depends()
):
    return await service.get_review_by_id(review_id)


@router.get('', response_model=ReviewPage, response_model_exclude_none=True, response_model_exclude_unset=True)
async def get_review_list(
        commons: dict = Depends(pagination),
        service: ReviewService = Depends()
):
    review_list, total = await service.get_review_list(commons)
    result = {"data": review_list,
              "total": total}
    for key, val in commons.items():
        if val is not None:
            result[key] = val
    return result
