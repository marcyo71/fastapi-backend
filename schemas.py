from pydantic import BaseModel, EmailStr
import enum

class UserStatus(str, enum.Enum):
    abbonato = "abbonato"
    attivo = "attivo"
    sospeso = "sospeso"
    free = "free"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: str
    status: UserStatus

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True