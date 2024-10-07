from pydantic import BaseModel
from datetime import datetime


# Schema for BLS Import model
class BlsImportModel(BaseModel):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
