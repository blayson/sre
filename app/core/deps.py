from typing import Optional


async def pagination(
        q: Optional[str] = None,
        page: int = 0,
        size: int = 100,
        start: Optional[int] = None,
        end: Optional[int] = None,
        sort: Optional[str] = None,
        feature: Optional[str] = None,
        product: Optional[str] = None
):

    return {"q": q,
            "page": None if start or end else page,
            "size": None if start or end else size,
            "start": start,
            "end": end,
            "sort": sort,
            "product": product,
            "feature": feature}


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, page: int = 0, limit: int = 100):
        self.q = q
        self.page = page
        self.limit = limit
