from fastapi import APIRouter
import stripe
from app.config.settings import settings

router = APIRouter(prefix="/api/stripe", tags=["stripe"])

stripe.api_key = settings.stripe_secret_key

@router.get("/events")
async def get_events():
    events = stripe.Event.list(limit=20)
    return events.data

