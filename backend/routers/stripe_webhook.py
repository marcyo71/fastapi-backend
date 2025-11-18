from fastapi import APIRouter, Request, HTTPException
import stripe
from app.stripe_config import STRIPE_WEBHOOK_SECRET
from app.backend.db import SessionLocal
from app.backend.models.transaction import Transaction

router = APIRouter()
stripe.api_key = stripe.api_key  # già impostata nel router, se serve puoi importarla

@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Webhook signature verification failed")

    # 🎯 Gestione evento
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session.get("id")
        customer_email = session.get("customer_email")
        amount_total = session.get("amount_total")

        db = SessionLocal()
        existing = db.query(Transaction).filter_by(session_id=session_id).first()
        if not existing:
            transaction = Transaction(
                session_id=session_id,
                customer_email=customer_email,
                amount_total=amount_total,
                status="paid"
            )
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            print(f"✅ Transazione salvata: {transaction}")
        else:
            print(f"ℹ️ Transazione già esistente: {existing.session_id}")

        print(f"✅ Pagamento completato: session_id={session_id}, email={customer_email}, importo={amount_total}")

    return {"status": "success"}
