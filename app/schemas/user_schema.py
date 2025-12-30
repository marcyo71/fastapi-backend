from pydantic import BaseModel, EmailStr
from datetime import datetime

# Input per registrazione
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

# Input per login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Output sicuro (non include hashed_password)
class UserRead(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
