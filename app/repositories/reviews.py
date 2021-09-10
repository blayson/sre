import typing

from sqlalchemy import select, func, types, insert
from sqlalchemy.sql import expression
from sqlalchemy.sql.functions import now, coalesce

from app.models.domain.tables import products, reviews, feature_names, \
    product_categories, reviews_suggestions, reviews_suggestions_states

from app.core.db import database
from app.models.schemas.reviews import ReviewUpdates
from app.models.schemas.users import User
from app.repositories.base import BaseRepository


class ReviewsRepository(BaseRepository):

    async def get_reviews(self, common_args: dict) -> typing.List[typing.Mapping]:
        join = reviews.join(products, products.c.products_id == reviews.c.products_id, isouter=True).join(
            feature_names, feature_names.c.feature_names_id == reviews.c.feature_names_id, isouter=True).join(
            reviews_suggestions, reviews_suggestions.c.reviews_id == reviews.c.reviews_id, isouter=True).join(
            reviews_suggestions_states,
            reviews_suggestions_states.c.reviews_suggestions_states_id == reviews_suggestions.c.reviews_suggestions_states_id, isouter=True)

        selectable = [reviews.c.text,
                      reviews.c.sentiment,
                      products.c.name.label('product'),
                      feature_names.c.text.label('feature'),
                      reviews.c.published_at,
                      coalesce(reviews_suggestions_states.c.name, None).label('status'),
                      func.concat(expression.cast(reviews.c.reviews_id, types.Unicode),
                                  expression.cast("|", types.Unicode),
                                  expression.cast(feature_names.c.feature_names_id, types.Unicode)).label('id'),
                      func.count().over().label('total_items')]

        sortable = {
            'sentiment': reviews.c.sentiment,
            'product': products.c.name,
            'feature': feature_names.c.text,
            'date': reviews.c.published_at
        }

        filterable = {
            'product': products.c.name,
            'feature': feature_names.c.text,
            'text': reviews.c.text,
            'pcat': products.c.product_categories_id,
            'status': reviews_suggestions_states.c.name,
        }
        if common_args['status'] and common_args['status'] == 'reviewed':
            selectable.append(reviews_suggestions.c.reviews_suggestions_id.label("suggestions_id"))

        query = select(selectable).select_from(join)

        if common_args['start'] or common_args['end']:
            query = self.paginate(query, common_args['start'], common_args['end'], False)
        else:
            query = self.paginate(query, common_args['page'], common_args['size'], True)

        if common_args['sort']:
            query = self.apply_sort(query, common_args['sort'], sortable)
        else:
            query = self.apply_sort(query, 'date desc', sortable)

        if common_args['product']:
            query = self.filter(query, ('product', common_args['product']), filterable)

        if common_args['feature']:
            query = self.filter(query, ('feature', common_args['feature']), filterable)

        if common_args['text']:
            query = self.filter(query, ('text', common_args['text']), filterable)

        if common_args['pcat']:
            query = self.filter_by_pcategory(query, ('pcat', common_args['pcat']), filterable)

        if common_args['status']:
            # status_stmt = reviews_suggestions_states.select(reviews_suggestions_states.c.name)
            # rows = await database.fetch_all(status_stmt)
            # if common_args['status'] in rows:
            query = self.filter_by_status(query, ("status", common_args['status']), filterable)
            # else:
            #     raise "There is no such status"
        else:
            query = query.where(reviews_suggestions.c.reviews_id.is_(None))
        print(query)

        return await database.fetch_all(query)

    @staticmethod
    async def get_review_by_id(review_id: int) -> typing.Optional[typing.Mapping]:
        query = reviews.select().where(review_id == reviews.c.reviews_id)
        return await database.fetch_one(query)

    @staticmethod
    async def get_product_categories():
        query = select([product_categories.c.product_categories_id.label('id'),
                        product_categories.c.czech_name.label('product_category')]).select_from(product_categories)
        return await database.fetch_all(query)

    @staticmethod
    async def submit_update(review_id, updates: ReviewUpdates, user: User):
        query_states = select([reviews_suggestions_states.c.reviews_suggestions_states_id]).select_from(
            reviews_suggestions_states).where(reviews_suggestions_states.c.name.ilike('pending'))

        row = await database.fetch_one(query_states)

        to_update = {"users_id": user.users_id, "suggestion_time": now(), "reviews_id": review_id,
                     "reviews_suggestions_states_id": row[0]}
        if updates.sentiment:
            to_update["sentiment"] = updates.sentiment.new_value

        if updates.feature:
            select_stmt = select([feature_names.c.feature_names_id]).select_from(feature_names).where(
                feature_names.c.text.ilike(updates.feature.new_value))

            feature_names_id = await database.fetch_one(select_stmt)
            to_update["feature_names_id"] = feature_names_id[0]

        if updates.product:
            to_update["product"] = ""

        insert_stmt = insert(reviews_suggestions).values(**to_update)

        return await database.execute(insert_stmt)
        # do_update_stmt = insert_stmt.on_conflict_do_update(
        #     constraint='reviews_id ',
        #     set_=dict(
        #         users_id=user.users_id,
        #         suggestion_time=now(),
        #         sentiment=updates.sentiment.new_value,
        #         feature_names_id=updates.feature.new_value,
        #         reviews_suggestions_states_id=row[0].reviews_suggestions_states_id
        #     ))
