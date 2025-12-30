import stripe
from fastapi import APIRouter, Request, Response, Form
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from typing import List

router = APIRouter(prefix="/payments", tags=["payments"])
templates = Jinja2Templates(directory="app/templates")

# Configura Stripe con le chiavi dal settings
stripe.api_key = settings.stripe_secret_key
public_key = settings.stripe_public_key

# Lista globale per la dashboard locale (solo debug)
stripe_events: List[dict] = []

# -------------------------------------------------------------------
# Checkout Session reale con Google Pay abilitato
# -------------------------------------------------------------------
@router.post("/create-checkout-session")
def create_checkout_session(plan: str = Form(...)):
    try:
        session = stripe.checkout.Session.create(
            mode="payment",
            automatic_payment_methods={"enabled": True},  # abilita Google Pay
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": plan},
                    "unit_amount": 1000,  # 10,00 €
                },
                "quantity": 1,
            }],
            success_url="http://localhost:5173/checkout-success",
            cancel_url="http://localhost:5173/checkout-cancel",
        )
        return {"checkout_url": session.url}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

# -------------------------------------------------------------------
# Endpoint per la Dashboard locale (solo debug)
# -------------------------------------------------------------------
@router.get("/events")
async def get_events():
    return stripe_events

# -------------------------------------------------------------------
# Success & Cancel
# -------------------------------------------------------------------
@router.get("/success")
async def payment_success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@router.get("/cancel")
async def payment_cancel(request: Request):
    return templates.TemplateResponse("cancel.html", {"request": request})

