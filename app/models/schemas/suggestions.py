import datetime
from typing import Optional, List

from app.models.schemas.base import BaseSchema, CommonArgs


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


class SuggestionForApprove(BaseSchema):
    reviews_suggestions_id: int
    users_id: int
    suggestion_time: datetime.date
    reviews_id: int
    changes: Changes
    state: str


class SuggestionsForApprove(CommonArgs):
    data: List[SuggestionForApprove]
