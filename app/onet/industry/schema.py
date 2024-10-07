from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Schema for creating a new ONET Industry
class OnetIndustryCreate(BaseModel):
    title: str
    code: str

    class Config:
        from_attributes = True


# Schema for updating an existing ONET Industry
class OnetIndustryUpdate(BaseModel):
    title: Optional[str] = None
    code: Optional[str] = None

    class Config:
        from_attributes = True


# Schema for displaying ONET industry data fetched from the API
class OnetIndustryModel(BaseModel):
    id: str
    title: str
    code: str
    createdAt: datetime
    updatedAt: datetime
