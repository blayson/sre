import typing

from sqlalchemy import select

from app.models.domain.tables import feature_names
from app.models.schemas.features import FeatureTable
from app.repositories.base import BaseRepository
from app.utils.db import database


class FeaturesRepository(BaseRepository):
    @staticmethod
    async def get_all_feature_names() -> typing.Dict[str, FeatureTable]:
        feature_stmt = select(
            [feature_names.c.text, feature_names.c.feature_names_id]
        ).select_from(feature_names)
        features_q = await database.fetch_all(feature_stmt)
        return {
            feature["feature_names_id"]: FeatureTable(**feature)
            for feature in features_q
        }
