from typing import Dict, List

from app.models.schemas.base import BaseSchema


class FeatureTable(BaseSchema):
    feature_names_id: int
    text: str


class FeatureNamesData(BaseSchema):
    value: int
    label: str


class FeatureNamesResponse(BaseSchema):
    data: List[FeatureNamesData]

