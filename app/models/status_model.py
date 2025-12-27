from pydantic import BaseModel
from app.db.base_class import Base

class StatusResponse(BaseModel):
    status: str

    class Config:
        from_attributes = True
