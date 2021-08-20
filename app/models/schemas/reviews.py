import datetime
from typing import List, Optional

from app.models.schemas.base import BaseSchemaORM, BaseSchema


class BaseFeature(BaseSchemaORM):
    text: str
    language: str
    cluster: str
    category: str
    description: str


class Feature(BaseSchemaORM):
    feature_names_id: int


class BaseProduct(BaseSchemaORM):
    name: str
    brand: str
    model: str
    introduced: str
    url_img: str
    url_web: str
    category: str
    retrieved_at: str
    inserted_at: str


class Product(BaseProduct):
    products_id: int


class BaseReview(BaseSchema):
    text: str
    sentiment: str
    published_at: datetime.date
    retrieved_at: datetime.date
    inserted_at: datetime.date


class Review(BaseReview):
    reviews_id: int
    mongo_id: str
    feature_names_id: int
    products_id: int


class ReviewExt(BaseReview):
    product: Product
    feature: Feature


class ReviewProduct(Review):
    brand: str
    model: str
    feature: str
    product_name: str


class ReviewTable(BaseSchema):
    feature: str
    product: str
    text: str
    sentiment: str


class ReviewPage(BaseSchemaORM):
    data: List[ReviewTable]
    page: Optional[int] = None
    size: Optional[int] = None
    total: int
    start: Optional[int] = None
    end: Optional[int] = None
    product: Optional[str] = None
    feature: Optional[str] = None

