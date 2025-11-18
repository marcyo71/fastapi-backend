from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    ref_code: str
    ref_by: str | None = None

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    balance: float
    ref_code: str
    ref_by: str | None = None

    class Config:
        from_attributes = True  # ✅ Pydantic v2

class UserReadMinimal(BaseModel):
    id: int
    name: str
    balance: float
    referrals: int  # 🔥 aggiunto per ranking

    class Config:
        from_attributes = True
