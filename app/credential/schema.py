from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Schema for creating a new Credential
class CredentialCreate(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


# Schema for updating an existing Credential
class CredentialUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True


# Response model to include timestamps and ID
class CredentialModel(CredentialCreate):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
