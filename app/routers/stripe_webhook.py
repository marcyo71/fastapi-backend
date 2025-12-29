from fastapi import APIRouter, Request, HTTPException
from app.config.settings import settings
import stripe

router = APIRouter(tags=["stripe"])

# Configura la chiave segreta Stripe
stripe.api_key = settings.stripe_secret_key

# Endpoint webhook
@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        # Verifica la firma del webhook
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.stripe_webhook_secret  # definiscila in debug_settings.py
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

    # Gestione eventi
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print(f"✅ Pagamento completato per sessione {session['id']}")

    elif event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        print(f"💰 PaymentIntent riuscito: {intent['id']}")

    else:
        print(f"ℹ️ Evento non gestito: {event['type']}")

    return {"status": "success"}
