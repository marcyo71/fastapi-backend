from pydantic import BaseModel
from datetime import datetime

class PaymentBase(BaseModel):
    session_id: str
    amount: int
    method: str
    status: str

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
