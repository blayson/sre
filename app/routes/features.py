from fastapi import APIRouter, Depends

from app.models.schemas.features import FeatureNamesResponse
from app.services.features import FeaturesService
from app.utils.constants import LanguagesQueryParameter

router = APIRouter()


@router.get("/match/{query}", response_model=FeatureNamesResponse)
async def get_all_feature_names(
    query: str,
    review_id: int,
    lang: LanguagesQueryParameter,
    service: FeaturesService = Depends(),
):
    review_list = await service.get_all_feature_names_by_lang(lang, review_id, query)
    return {"data": review_list}