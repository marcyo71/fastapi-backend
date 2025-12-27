from pydantic import BaseModel

class PayoutResponse(BaseModel):
    status: str
    amount: float

    class Config:
        from_attributes = True  # ✅ compatibile con Pydantic v2
