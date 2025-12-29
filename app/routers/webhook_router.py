import stripe
from fastapi import APIRouter, Request, HTTPException
from app.settings import settings

router = APIRouter()

@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.stripe_webhook_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload")

    # --- PROCESSA L'EVENTO ---
    match event["type"]:

        # ---------------------------------------------------------
        # Pagamento singolo completato
        # ---------------------------------------------------------
        case "checkout.session.completed":
            session = event["data"]["object"]
            print("CHECKOUT COMPLETED:", session["id"])
            # TODO: salva ordine / pagamento nel DB

        # ---------------------------------------------------------
        # Subscription creata
        # ---------------------------------------------------------
        case "customer.subscription.created":
            subscription = event["data"]["object"]
            print("SUBSCRIPTION CREATED:", subscription["id"])
            # TODO: salva subscription nel DB

        # ---------------------------------------------------------
        # Subscription aggiornata (cambio piano, rinnovo, trial, ecc.)
        # ---------------------------------------------------------
        case "customer.subscription.updated":
            subscription = event["data"]["object"]
            print("SUBSCRIPTION UPDATED:", subscription["id"])
            # TODO: aggiorna stato subscription nel DB

        # ---------------------------------------------------------
        # Subscription cancellata
        # ---------------------------------------------------------
        case "customer.subscription.deleted":
            subscription = event["data"]["object"]
            print("SUBSCRIPTION DELETED:", subscription["id"])
            # TODO: aggiorna DB → status = "canceled"

        # ---------------------------------------------------------
        # Pagamento subscription riuscito
        # ---------------------------------------------------------
        case "invoice.payment_succeeded":
            invoice = event["data"]["object"]
            print("INVOICE PAID:", invoice["id"])
            # TODO: aggiorna next billing date

        # ---------------------------------------------------------
        # Pagamento subscription fallito
        # ---------------------------------------------------------
        case "invoice.payment_failed":
            invoice = event["data"]["object"]
            print("INVOICE FAILED:", invoice["id"])
            # TODO: notifica utente / sospendi servizio

        # ---------------------------------------------------------
        # Eventi non gestiti
        # ---------------------------------------------------------
        case _:
            print("EVENTO NON GESTITO:", event["type"])

    return {"status": "success"}
