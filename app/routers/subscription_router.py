import stripe
from fastapi import APIRouter, Form, HTTPException
from app.config.settings import settings

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

stripe.api_key = settings.stripe_secret_key

# -------------------------------------------------------------------
# Crea una Checkout Session per un abbonamento
# -------------------------------------------------------------------
@router.post("/create-checkout-session")
def create_subscription_session(price_id: str = Form(...), customer_email: str = Form(...)):
    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            customer_email=customer_email,
            line_items=[{
                "price": price_id,
                "quantity": 1
            }],
            success_url="http://localhost:5173/subscription-success",
            cancel_url="http://localhost:5173/subscription-cancel",
        )
        return {"checkout_url": session.url}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

