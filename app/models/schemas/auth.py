from app.models.schemas.base import BaseSchemaORM


class Token(BaseSchemaORM):
    token: str
