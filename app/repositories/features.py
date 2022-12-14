import typing

from sqlalchemy import select

from app.models.domain.tables import feature_names, languages
from app.models.schemas.features import FeatureTable
from app.repositories.base import BaseRepository
from app.utils.constants import LanguagesQueryParameter
from app.utils.db import database


class FeaturesRepository(BaseRepository):
    async def get_all_feature_names_by_lang(self, lang: LanguagesQueryParameter) -> typing.Dict[str, FeatureTable]:
        feature_stmt = select(
            [feature_names.c.text, feature_names.c.feature_names_id]
        ).select_from(
            feature_names.join(
                languages,
                languages.c.languages_id == feature_names.c.languages_id
            )
        )

        feature_stmt = self.filter_by_lang(feature_stmt, lang)
        features_q = await database.fetch_all(feature_stmt)
        return {
            feature["feature_names_id"]: FeatureTable(**feature)
            for feature in features_q
        }
