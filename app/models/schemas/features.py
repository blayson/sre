from typing import Dict

from app.models.schemas.base import BaseSchema


class FeatureTable(BaseSchema):
    feature_names_id: int
    text: str


class FeatureNamesResponse(BaseSchema):
    data: Dict[str, FeatureTable]
