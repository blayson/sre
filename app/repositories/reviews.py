import typing

from sqlalchemy import select, func, asc, desc
from app.models.domain.tables import products, reviews, product_names, product_features_keywords, feature_names

from app.core.db import database
from app.repositories.base import BaseRepository


class ReviewsRepository(BaseRepository):

    async def get_reviews(self, common_args: dict) -> typing.List[typing.Mapping]:
        join = reviews.join(products, products.c.products_id == reviews.c.products_id, isouter=True).join(
            product_names, product_names.c.products_id == products.c.products_id, isouter=True).join(
            product_features_keywords, product_features_keywords.c.products_id == products.c.products_id).join(
            feature_names, feature_names.c.feature_names_id == product_features_keywords.c.feature_names_id)

        selectable = [reviews.c.text,
                      reviews.c.sentiment,
                      products.c.name.label('product'),
                      feature_names.c.text.label('feature'),
                      func.count().over().label('total_items')]

        sortable = {
            'sentiment': reviews.c.sentiment,
            'product': products.c.name,
            'feature': feature_names.c.text
        }
        filterable = {
            'product': products.c.name,
            'feature': feature_names.c.text
        }

        query = select(selectable).select_from(join)

        if common_args['start'] or common_args['end']:
            query = self.paginate_range(query, common_args['start'], common_args['end'])
        else:
            query = self.paginate(query, common_args['page'], common_args['size'])

        if common_args['sort']:
            query = self.apply_sort(query, common_args['sort'], sortable)

        if common_args['product']:
            query = self.filter(query, ('product', common_args['product']), filterable)

        if common_args['feature']:
            query = self.filter(query, ('feature', common_args['feature']), filterable)

        return await database.fetch_all(query=query)

    @staticmethod
    async def get_review_by_id(review_id: int) -> typing.Optional[typing.Mapping]:
        query = reviews.select().where(review_id == reviews.c.reviews_id)
        return await database.fetch_one(query)
