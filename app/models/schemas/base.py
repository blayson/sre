from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseSchemaORM(BaseModel):
    class Config:
        orm_mode = True
        json_encoders = {
            # Add custom decoders that you need here
            datetime: lambda dt: dt.timestamp(),
        }


class BaseSchema(BaseModel):
    pass


class CommonArgs(BaseSchema):
    page: Optional[int] = None
    size: Optional[int] = None
    total: int = 0
    start: Optional[int] = None
    end: Optional[int] = None
    product: Optional[str] = None
    feature: Optional[str] = None
    text: Optional[str] = None
