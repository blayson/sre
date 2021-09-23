import datetime
from typing import Optional

from app.models.schemas.base import BaseSchema


class Review(BaseSchema):
    reviews_id: int


class User(BaseSchema):
    users_id: int
    name: str


class ChangesValues(BaseSchema):
    old_value: str
    new_value: str


class Changes(BaseSchema):
    sentiment: Optional[ChangesValues]
    feature_names: Optional[ChangesValues]
    product: Optional[ChangesValues]


class UserReviewsSuggestions(BaseSchema):
    reviews_suggestions_id: int
    user: User
    suggestion_time: datetime.date
    review: Review
    changes: Changes
    reviews_suggestions_states: str
