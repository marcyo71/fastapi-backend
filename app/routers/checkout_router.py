from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
import stripe
from app.core.config import settings

router = APIRouter(prefix="/api/checkout", tags=["checkout"])

stripe.api_key = settings.stripe_secret_key

@router.post("/create-checkout-session", response_class=JSONResponse)
async def create_checkout_session(request: Request):
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {"name": "Prodotto di test"},
                "unit_amount": 1000,
            },
            "quantity": 1,
        }],
        payment_method_options={"klarna": {}},
        success_url="http://localhost:5173/checkout-success",
        cancel_url="http://localhost:5173/checkout-cancel",
    )

    # Se la richiesta arriva da browser (HTML)
    if "text/html" in request.headers.get("accept", ""):
        return HTMLResponse(f"""
            <html>
                <body>
                    <a href="{session.url}">Vai al checkout</a>
                </body>
            </html>
        """)

    # Se arriva da React → JSON
    return {"url": session.url}
