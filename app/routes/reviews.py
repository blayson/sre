from fastapi import APIRouter, Depends

from app.models.schemas.reviews import (
    ProductCategories,
    Review,
    ReviewPage,
    ReviewSuggestions,
)
from app.models.schemas.users import User
from app.services.reviews import ReviewService
from app.utils.deps import get_current_user, pagination
from app.utils.utils import propagate_args

router = APIRouter()


@router.get("", response_model=ReviewPage, response_model_exclude_unset=True)
async def get_review_list(
    commons: dict = Depends(pagination),
    service: ReviewService = Depends(),
    user: User = Depends(get_current_user),
):
    review_list, total = await service.get_review_list(commons, user)
    result = {"data": review_list, "total": total}
    propagate_args(common_args=commons, resp=result)
    return result


@router.get("/categories", response_model=ProductCategories)
async def get_review_list(service: ReviewService = Depends()):
    return await service.get_categories_list()


@router.get("/{review_id}/suggestions")
async def get_review_suggestions(review_id: int, service: ReviewService = Depends()):
    status = await service.get_review_suggestions(review_id)
    if status:
        return {"status": "Ok"}
    else:
        return {"status": "error"}


@router.get("/{review_id}", response_model=Review)
async def get_review(review_id: int, service: ReviewService = Depends()):
    return await service.get_review_by_id(review_id)
