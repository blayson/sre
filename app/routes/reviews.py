from fastapi import APIRouter, Depends

from app.core.deps import pagination
from app.models.schemas.reviews import Review, ReviewPage, ProductCategories, ReviewUpdates
from app.models.schemas.users import User
from app.services.auth import get_current_user
from app.services.reviews import ReviewService

router = APIRouter()


@router.get('', response_model=ReviewPage, response_model_exclude_unset=True)
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


@router.get('/categories', response_model=ProductCategories)
async def get_review_list(
        service: ReviewService = Depends()
):
    return await service.get_categories_list()


@router.post('/{review_id}/updates/submit')
async def update_review(
        review_id: int,
        updates: ReviewUpdates,
        service: ReviewService = Depends(),
        user: User = Depends(get_current_user)
):
    status = await service.submit_update(review_id, updates, user)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.post('/{review_id}/updates/approve')
async def update_review(
        review_id: int,
        service: ReviewService = Depends()
):
    status = await service.approve_update(review_id)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.post('/{review_id}/updates/reject')
async def update_review(
        review_id: int,
        service: ReviewService = Depends()
):
    status = await service.reject_update(review_id)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.post('/{review_id}/updates')
async def update_review(
        review_id: int,
        service: ReviewService = Depends()
):
    status = await service.get_updates_by_review(review_id)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.post('/updates/{update_id}')
async def update_review(
        update_id: int,
        service: ReviewService = Depends()
):
    status = await service.get_update_by_id(update_id)
    if status:
        return {'status': 'Ok'}
    else:
        return {'status': 'error'}


@router.post('/updates')
async def update_review(
        service: ReviewService = Depends()
):
    status = await service.get_all_updates()
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
