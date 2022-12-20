from typing import List

from fastapi import Depends

from app.models.schemas.features import FeatureNamesData
from app.repositories.features import FeaturesRepository
from app.services.base import BaseService
from app.utils.constants import LanguagesQueryParameter


class FeaturesService(BaseService):
    def __init__(self, repository: FeaturesRepository = Depends()):
        self.repository: FeaturesRepository = repository

    async def get_all_feature_names_by_lang(
        self, lang: LanguagesQueryParameter, review_id: int, query: str
    ) -> List[FeatureNamesData]:
        features_dict = await self.repository.get_all_feature_names_by_lang(lang, review_id, query.lower())
        return [
            FeatureNamesData(value=int(feature_id), label=feature_table.text)
            for feature_id, feature_table in features_dict.items()
        ]
