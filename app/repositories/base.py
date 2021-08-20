from sqlalchemy import asc, desc


class BaseRepository:

    @staticmethod
    def paginate(query, page: int, size: int):
        query = query.limit(size).offset(page * size)
        return query

    @staticmethod
    def paginate_range(query, start: int, end: int):
        query = query.limit(end - start).offset(start)
        return query

    @staticmethod
    def apply_sort(query, sort_arg: str, sortable: dict):
        sort_arr = sort_arg.split(',')
        for sort in sort_arr:
            column, sort_type = sort.split(' ')
            if sort_type == 'asc':
                query = query.order_by(asc(sortable[column]))
            elif sort_type == 'desc':
                query = query.order_by(desc(sortable[column]))
        return query

    @staticmethod
    def filter(query, filter_args: tuple, filterable: dict):
        return query.where(filterable[filter_args[0]].ilike('%' + filter_args[1] + '%'))
