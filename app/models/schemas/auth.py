from app.models.schemas.base import BaseSchema


class Token(BaseSchema):
    token: str
