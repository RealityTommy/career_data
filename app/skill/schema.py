from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Schema for creating a new Skill
class SkillCreate(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True  # Replaces orm_mode in Pydantic v2


# Schema for updating an existing Skill
class SkillUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# Response model to include timestamps and ID
class SkillModel(SkillCreate):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
