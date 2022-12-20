import typing

from sqlalchemy import select, and_

from app.models.domain.tables import feature_names, languages, reviews, product_categories, products
from app.models.schemas.features import FeatureTable
from app.repositories.base import BaseRepository
from app.utils.constants import LanguagesQueryParameter
from app.utils.db import database


class FeaturesRepository(BaseRepository):
    async def get_all_feature_names_by_lang(
        self, lang: LanguagesQueryParameter, review_id: int, query: str
    ) -> typing.Dict[str, FeatureTable]:
        review_stmt = select([products.c.product_categories_id]).select_from(
            reviews.join(products, products.c.products_id == reviews.c.products_id)
        ).where(reviews.c.reviews_id == review_id)

        product_category_id = await database.fetch_val(review_stmt)

        feature_stmt = select(
            [feature_names.c.text, feature_names.c.feature_names_id]
        ).select_from(
            feature_names.join(
                languages, languages.c.languages_id == feature_names.c.languages_id
            )
        ).where(and_(feature_names.c.product_categories_id == product_category_id, feature_names.c.text.ilike(f"%{query}%")))

        feature_stmt = self.filter_by_lang(feature_stmt, lang)
        features_q = await database.fetch_all(feature_stmt)
        return {
            feature["feature_names_id"]: FeatureTable(**feature)
            for feature in features_q
        }
