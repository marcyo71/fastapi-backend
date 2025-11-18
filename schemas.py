from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    name: str
    status: str

class UserRead(UserCreate):
    id: int
    class Config:
        orm_mode = True

class TransactionCreate(BaseModel):
    session_id: str
    customer_email: str
    amount_total: int
    status: str
    amount: float
    currency: str
    user_id: int

class TransactionRead(TransactionCreate):
    id: int
    class Config:
        orm_mode = True
