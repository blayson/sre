from typing import Mapping, Optional, List

from fastapi import Depends

from app.models.schemas.features import FeatureNamesData
from app.repositories.features import FeaturesRepository
from app.services.base import BaseService
from app.utils.constants import LanguagesQueryParameter


class FeaturesService(BaseService):
    def __init__(self, repository: FeaturesRepository = Depends()):
        self.repository: FeaturesRepository = repository

    async def get_all_feature_names_by_lang(self, lang: LanguagesQueryParameter) -> List[FeatureNamesData]:
        features_dict = await self.repository.get_all_feature_names_by_lang(lang)
        return [FeatureNamesData(value=int(feature_id), label=feature_table.text) for feature_id, feature_table in features_dict.items()]
