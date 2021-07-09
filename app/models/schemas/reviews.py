from typing import List

from app.models.schemas.base import BaseSchema


class BaseFeature(BaseSchema):
    text: str
    language: str
    cluster: str
    category: str
    description: str


class Feature(BaseSchema):
    feature_names_id: int


class BaseProduct(BaseSchema):
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
    published_at: str
    retrieved_at: str
    inserted_at: str


class Review(BaseReview):
    reviews_id: int
    mongo_id: int
    feature_names_id: int
    products_id: int


class ReviewExt(BaseReview):
    product: Product
    feature: Feature


class ReviewList(BaseSchema):
    __root__: List[Review]


class ReviewPage(ReviewList):
    page: int
    size: int
    total: int

