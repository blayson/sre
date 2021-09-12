from sqlalchemy import asc, desc

from app.models.domain.tables import reviews_suggestions
from app.models.schemas.users import User


class BaseRepository:

    @staticmethod
    def paginate(query, start: int, end: int, page: bool):
        if page:
            query = query.limit(end).offset(start * end)
        else:
            query = query.limit(end - start).offset(start)
        return query

    @staticmethod
    def apply_sort(query, sort_arg: str, sortable: dict):
        sort_arr = sort_arg.split(',')
        for sort in sort_arr:
            sort_parsed = sort.split(' ')
            column = sort_parsed[0]
            try:
                sort_type = sort_parsed[1]
            except IndexError:
                sort_type = 'asc'

            if sort_type == 'asc':
                query = query.order_by(asc(sortable[column]))
            elif sort_type == 'desc':
                query = query.order_by(desc(sortable[column]))
        return query

    @staticmethod
    def filter(query, filter_args: tuple, filterable: dict):
        return query.where(filterable[filter_args[0]].ilike('%' + filter_args[1] + '%'))

    @staticmethod
    def filter_by_pcategory(query, filter_args: tuple, filterable: dict):
        query = query.where(filterable[filter_args[0]] == filter_args[1])
        return query

    @staticmethod
    def filter_by_status(query, filter_args: tuple, filterable: dict, user: User):
        status = ''
        if filter_args[1] == 'reviewed':
            return query.where(filterable[filter_args[0]].ilike('%pending%')
                               | filterable[filter_args[0]].ilike('%approved%')
                               | filterable[filter_args[0]].ilike('%rejected%'))\
                .where(reviews_suggestions.c.users_id == user.users_id)
        elif filter_args[1] == 'rejected':
            status = 'rejected'
        elif filter_args[1] == 'approved':
            status = 'approved'
        elif filter_args[1] == 'notReviewed':
            return query.where(reviews_suggestions.c.reviews_id.is_(None))
        elif filter_args[1] == 'all':
            return query

        query = query.where(filterable[filter_args[0]].ilike('%' + status + '%'))
        return query
