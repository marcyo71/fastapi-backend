from pydantic import BaseModel, EmailStr
from datetime import datetime


# -------------------------
# Base
# -------------------------
class UserBase(BaseModel):
    email: EmailStr


# -------------------------
# Create
# -------------------------
class UserCreate(UserBase):
    password: str


# -------------------------
# Update
# -------------------------
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


# -------------------------
# Read
# -------------------------
class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
