from pydantic import BaseModel
from datetime import datetime


# Schema for creating a new ONET Occupation
class OnetOccupationCreate(BaseModel):
    title: str
    code: str

    class Config:
        from_attributes = True


# Schema for updating an existing ONET Occupation
class OnetOccupationUpdate(BaseModel):
    title: str
    code: str

    class Config:
        from_attributes = True


# Schema for displaying ONET occupation data fetched from the API (without id, createdAt, updatedAt)
class OnetOccupationAPISchema(BaseModel):
    title: str
    code: str

    class Config:
        from_attributes = True


# Schema for returning Occupation data in API responses from the database (with id, createdAt, updatedAt)
class OnetOccupationModel(BaseModel):
    id: str
    title: str
    code: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
