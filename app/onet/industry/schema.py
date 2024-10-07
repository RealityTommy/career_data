from pydantic import BaseModel
from datetime import datetime


# Schema for creating a new ONET Industry
class OnetIndustryCreate(BaseModel):
    title: str
    code: str

    class Config:
        from_attributes = True


# Schema for updating an existing ONET Industry
class OnetIndustryUpdate(BaseModel):
    title: str
    code: str

    class Config:
        from_attributes = True


# Schema for displaying ONET industry data fetched from the API (without id, createdAt, updatedAt)
class OnetIndustryAPISchema(BaseModel):
    title: str
    code: str

    class Config:
        from_attributes = True


# Schema for returning Industry data in API responses from the database (with id, createdAt, updatedAt)
class OnetIndustryModel(BaseModel):
    id: str
    title: str
    code: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
