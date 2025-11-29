from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ---- UserStatus ----
class UserStatusCreate(BaseModel):
    status: str = Field(..., min_length=2, max_length=32)

class UserStatusRead(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True

# ---- User ----
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=64)
    email: EmailStr
    status_id: int

class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    status_id: int

    class Config:
        from_attributes = True

# ---- Transaction ----
class TransactionCreate(BaseModel):
    user_id: int
    amount: float = Field(..., ge=0.0)

class TransactionRead(BaseModel):
    id: int
    user_id: int
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True

# ---- Referral ----
class ReferralCreate(BaseModel):
    referrer_id: int
    referred_id: int

class ReferralRead(BaseModel):
    id: int
    referrer_id: int
    referred_id: int
    created_at: datetime

    class Config:
        from_attributes = True
