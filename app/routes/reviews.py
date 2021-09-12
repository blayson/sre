from typing import Optional

from fastapi import APIRouter, Depends

from app.core.deps import pagination
from app.models.schemas.reviews import Review, ReviewPage, ProductCategories, ReviewSuggestions
from app.models.schemas.users import User
from app.services.auth import get_current_user
from app.services.reviews import ReviewService

router = APIRouter()


@router.get('', response_model=ReviewPage, response_model_exclude_unset=True)
async def get_review_list(
        commons: dict = Depends(pagination),
        service: ReviewService = Depends(),
        user: User = Depends(get_current_user)
):
    review_list, total = await service.get_review_list(commons, user)
    result = {"data": review_list,
              "total": total}
    for key, val in commons.items():
        if val is not None:
            result[key] = val
    return result


@router.get('/categories', response_model=ProductCategories)
async def get_review_list(
        service: ReviewService = Depends()
):
    return await service.get_categories_list()


@router.post('/{review_id}/suggestions/submit')
async def submit_review_suggestions(
        review_id: int,
        suggestions: ReviewSuggestions,
        service: ReviewService = Depends(),
        user: User = Depends(get_current_user),
        changes: Optional[bool] = True,
):
    status = await service.submit_suggestions(review_id, suggestions, user, changes)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.post('/{review_id}/suggestions')
async def get_review_suggestions(
        review_id: int,
        service: ReviewService = Depends()
):
    status = await service.get_review_suggestions(review_id)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.post('/suggestions/{suggestions_id}/approve')
async def approve_review_suggestions(
        review_id: int,
        service: ReviewService = Depends()
):
    status = await service.approve_suggestions(review_id)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.post('/suggestions/{suggestions_id}/reject')
async def reject_review_suggestions(
        review_id: int,
        service: ReviewService = Depends()
):
    status = await service.reject_suggestions(review_id)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.get('/{review_id}', response_model=Review)
async def get_review(
        review_id: int,
        service: ReviewService = Depends()
):
    return await service.get_review_by_id(review_id)
