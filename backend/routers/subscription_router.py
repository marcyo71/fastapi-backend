# backend/routers/subscription_router.py
from fastapi import APIRouter, Request, HTTPException
import stripe
from backend.config.settings import settings

router = APIRouter(prefix="/subscription", tags=["subscription"])

# Configura Stripe con la chiave segreta
stripe.api_key = settings.STRIPE_SECRET_KEY

@router.post("/create-checkout-session")
async def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": settings.STRIPE_PRICE_ID,
                "quantity": 1,
            }],
            success_url="http://localhost:8000/success",
            cancel_url="http://localhost:8000/cancel",
        )
        return {"checkout_url": checkout_session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Gestisci gli eventi principali
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(f"✅ Checkout completato: {session['id']}")

    elif event["type"] == "invoice.paid":
        invoice = event["data"]["object"]
        print(f"💰 Abbonamento pagato: {invoice['id']}")

    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        print(f"⚠️ Pagamento fallito: {invoice['id']}")

    return {"status": "success"}
