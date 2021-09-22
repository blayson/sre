from typing import Optional

from fastapi import Depends, HTTPException

from app.models.schemas.users import User
from app.services.auth import oauth2_scheme, AuthService


async def pagination(
        q: Optional[str] = None,
        page: int = 0,
        size: int = 100,
        start: Optional[int] = None,
        end: Optional[int] = None,
        sort: Optional[str] = None,
        feature: Optional[str] = None,
        product: Optional[str] = None,
        text: Optional[str] = None,
        pcat: Optional[int] = None,
        status: Optional[str] = None
):

    return {"q": q,
            "page": None if start or end else page,
            "size": None if start or end else size,
            "start": start,
            "end": end,
            "sort": sort,
            "product": product,
            "feature": feature,
            "text": text,
            "pcat": pcat,
            "status": status}


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, page: int = 0, limit: int = 100):
        self.q = q
        self.page = page
        self.limit = limit


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        service: AuthService = Depends()
) -> User:
    return await service.verify_token(token)


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.user_roles_id != 2:
        raise HTTPException(status_code=403, detail="Forbidden")
    return current_user
