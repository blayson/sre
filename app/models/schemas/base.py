from datetime import datetime

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
