class BaseService:

    @staticmethod
    def paginate(query, page: int, size: int):
        query = query.limit(size).offset(page*size)
        return query
