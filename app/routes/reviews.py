from fastapi import APIRouter, Depends

from app.models.schemas.reviews import ProductCategories, Review, ReviewPage
from app.models.schemas.users import User
from app.services.reviews import ReviewService
from app.utils.deps import get_current_user, pagination
from app.utils.utils import propagate_args

router = APIRouter()


@router.get(
    "",
    response_model=ReviewPage,
    response_model_exclude_unset=True,
    dependencies=[Depends(get_current_user)],
)
async def get_reviews(
    commons: dict = Depends(pagination),
    service: ReviewService = Depends(),
    user: User = Depends(get_current_user),
):
    review_list, total = await service.get_reviews(commons, user)
    result = {"data": review_list, "total": total}
    propagate_args(common_args=commons, resp=result)
    return result


@router.get(
    "/categories",
    response_model=ProductCategories,
    dependencies=[Depends(get_current_user)],
)
async def get_categories(service: ReviewService = Depends()):
    return await service.get_categories()


@router.get(
    "/{review_id}", response_model=Review, dependencies=[Depends(get_current_user)]
)
async def get_review(review_id: int, service: ReviewService = Depends()):
    return await service.get_review_by_id(review_id)
