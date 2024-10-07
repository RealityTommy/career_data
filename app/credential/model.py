from pydantic import BaseModel
from datetime import datetime


# Model used for returning Credential data in API responses
class CredentialModel(BaseModel):
    id: str
    name: str
    description: str | None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
