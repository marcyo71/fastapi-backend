from fastapi import APIRouter
import stripe
from app.core.config import settings

router = APIRouter(prefix="/api/stripe", tags=["stripe"])

# Imposta la chiave Stripe correttamente
stripe.api_key = settings.stripe_secret_key

@router.post("/create-payment-intent")
async def create_payment_intent(data: dict):
    amount = data.get("amount", 1000)
    currency = data.get("currency", "eur")

    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        automatic_payment_methods={"enabled": True}
    )

    return {"client_secret": intent.client_secret}

