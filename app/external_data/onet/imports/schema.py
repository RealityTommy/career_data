from pydantic import BaseModel
from datetime import datetime


# Schema for displaying OnetImport data
class OnetImportModel(BaseModel):
    id: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
