from pydantic import BaseModel
from datetime import datetime


# Model used for returning Industry data in API responses
class OnetIndustryModel(BaseModel):
    id: str
    title: str
    code: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
