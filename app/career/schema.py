from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# This is the schema for creating a new Career
class CareerCreate(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# This schema will be used for updating a Career, allowing partial updates
class CareerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# Model used for returning Career data in API responses
class CareerModel(BaseModel):
    id: str
    name: str
    description: str | None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
