import datetime
from typing import List, Optional, Union

from pydantic import Field, validator

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
    id: str
    feature: str
    product: str
    text: str
    sentiment: str
    published_at: datetime.date
    status: Optional[str] = None
    suggestions_id: Optional[int] = None


class ReviewPage(BaseSchemaORM):
    data: Optional[List[ReviewTable]] = []
    page: Optional[int] = None
    size: Optional[int] = None
    total: int = 0
    start: Optional[int] = None
    end: Optional[int] = None
    product: Optional[str] = None
    feature: Optional[str] = None
    text: Optional[str] = None


class ProductCategory(BaseSchema):
    id: int
    product_category: Optional[str]


class ProductCategories(BaseSchema):
    __root__: List[ProductCategory]


class UpdateData(BaseSchema):
    new_value: str = Field(None, alias='newValue')
    old_value: str = Field(None, alias='oldValue')


class ReviewUpdates(BaseSchema):
    index: int
    sentiment: Optional[UpdateData]
    feature: Optional[UpdateData]
    product: Optional[UpdateData]
