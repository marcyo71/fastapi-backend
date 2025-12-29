from fastapi import APIRouter
import stripe
from app.config.settings import settings

router = APIRouter(prefix="/api/payment", tags=["payment"])

stripe.api_key = settings.stripe_secret_key

@router.post("/create-intent")
async def create_intent():
    """
    Crea un PaymentIntent per il Payment Element.
    """
    intent = stripe.PaymentIntent.create(
        amount=1000,  # 10,00 €
        currency="eur",
        automatic_payment_methods={"enabled": True}
    )

    return {"clientSecret": intent.client_secret}

