from fastapi import APIRouter, Depends

from app.models.schemas.features import FeatureNamesResponse
from app.services.features import FeaturesService

router = APIRouter()


@router.get(
    "/names", response_model=FeatureNamesResponse
)
async def get_all_feature_names(
    service: FeaturesService = Depends(),
):
    review_list = await service.get_all_feature_names()
    return {"data": review_list}
