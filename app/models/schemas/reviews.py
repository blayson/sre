import datetime
from typing import List, Optional

from pydantic import Field

from app.models.schemas.base import BaseSchemaORM, BaseSchema, CommonArgs


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
    suggestion_time: Optional[datetime.date] = None


class ReviewPage(BaseSchemaORM, CommonArgs):
    data: Optional[List[ReviewTable]]


class ProductCategory(BaseSchema):
    id: int
    product_category: Optional[str]


class ProductCategories(BaseSchema):
    __root__: List[ProductCategory]


class SuggestionData(BaseSchema):
    new_value: str = Field(None, alias='newValue')
    old_value: str = Field(None, alias='oldValue')


class ReviewSuggestions(BaseSchema):
    reviews_id: int
    sentiment: Optional[SuggestionData]
    feature: Optional[SuggestionData]
