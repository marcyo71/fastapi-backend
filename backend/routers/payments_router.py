from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.dependencies import get_api_key

payments_router = APIRouter()

class PaymentCreate(BaseModel):
    amount: float
    user_id: int

@payments_router.post("/")
def create_payment(data: PaymentCreate, api_key: str = Depends(get_api_key)):
    return {"id": 1, "amount": data.amount, "user_id": data.user_id, "status": "pending"}

@payments_router.get("/")
def list_payments(api_key: str = Depends(get_api_key)):
    return [{"id": 1, "amount": 19.99, "status": "pending"}]
