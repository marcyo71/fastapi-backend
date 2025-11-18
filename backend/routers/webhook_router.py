from fastapi import APIRouter, Request, Header
from fastapi.responses import JSONResponse
import stripe

router = APIRouter()

# ⚠️ In produzione metti questo in .env
endpoint_secret = "YOUR_WEBHOOK_SECRET"

@router.post("/stripe-webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, endpoint_secret
        )
    except stripe.error.SignatureVerificationError:
        return JSONResponse({"error": "Invalid signature"}, status_code=400)

    # 🎯 Gestione eventi
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_email = session["customer_details"]["email"]

        # 🔄 Aggiorna DB: utente diventa abbonato
        # Esempio con SQLAlchemy:
        # user = db.query(User).filter(User.email == user_email).first()
        # if user:
        #     user.status = "abbonato"
        #     db.commit()

        print(f"✅ Pagamento completato per utente: {user_email}")

    return JSONResponse({"status": "success"})
