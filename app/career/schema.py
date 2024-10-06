from pydantic import BaseModel
from typing import Optional


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
