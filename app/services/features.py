from typing import Mapping, Optional

from fastapi import Depends

from app.repositories.features import FeaturesRepository
from app.services.base import BaseService


class FeaturesService(BaseService):
    def __init__(self, repository: FeaturesRepository = Depends()):
        self.repository: FeaturesRepository = repository

    async def get_all_feature_names(self) -> Optional[Mapping]:
        return await self.repository.get_all_feature_names()
