from pydantic import BaseModel
from datetime import datetime


# Model used for returning Career data in API responses
class IndustryModel(BaseModel):
    id: str
    name: str
    description: str | None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
