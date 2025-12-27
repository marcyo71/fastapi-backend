from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    amount: float
    type: str
    user_id: int

class TransactionOut(TransactionCreate):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2

class TransactionRead(BaseModel):
    id: int
    user_id: int
    amount: float
    method: str
    status: str
    provider_id: str
    created_at: datetime

    class Config:
        from_attributes = True
