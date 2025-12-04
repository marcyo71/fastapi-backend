from app import APIRouter, Depends
from pydantic import BaseModel
from backend.dependencies import get_api_key

stripe_router = APIRouter()

class CheckoutRequest(BaseModel):
    amount: float
    user_id: int

@stripe_router.post("/checkout")
def stripe_checkout(data: CheckoutRequest, api_key: str = Depends(get_api_key)):
    return {"session_id": "sess_123", "amount": data.amount, "user_id": data.user_id}
