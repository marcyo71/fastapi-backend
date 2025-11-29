from pydantic import BaseModel, EmailStr
from datetime import datetime

# ---------------------------
# User Schemas
# ---------------------------
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        from_attributes = True


# ---------------------------
# Transaction Schemas
# ---------------------------
class TransactionBase(BaseModel):
    description: str
    amount: float

class TransactionCreate(TransactionBase):
    user_id: int
    payment_id: int | None = None

class Transaction(TransactionBase):
    id: int
    created_at: datetime
    user_id: int | None = None
    payment_id: int | None = None
    class Config:
        from_attributes = True
