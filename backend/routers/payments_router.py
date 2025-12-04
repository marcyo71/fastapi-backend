import stripe
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from backend.config.settings import settings
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/payments", tags=["payments"])
templates = Jinja2Templates(directory="app/templates")

# Configura Stripe con la secret key
stripe.api_key = settings.stripe_secret_key

@router.get("/")
async def payment_page():
    return {"msg": "Area Pagamenti"}

@router.post("/create-checkout-session")
async def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": "Abbonamento Mensile"},
                    "unit_amount": 1000,  # €10
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="http://localhost:8000/payments/success",
            cancel_url="http://localhost:8000/payments/cancel",
        )
        return JSONResponse({"id": session.id})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except Exception:
        return Response(status_code=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        print("Pagamento riuscito:", session)

    return Response(status_code=200)

@router.get("/success")
async def payment_success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})

@router.get("/cancel")
async def payment_cancel(request: Request):
    return templates.TemplateResponse("cancel.html", {"request": request})