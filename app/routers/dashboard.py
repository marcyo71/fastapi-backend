from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db

router = APIRouter()

@router.get("/dashboard/events")
async def get_events(db: AsyncSession = Depends(get_db)):
    # Per ora dati finti, poi li prenderai dal DB
    return [
        {"type": "checkout.session.completed", "timestamp": "2025-12-22T14:54:06"},
        {"type": "payment_intent.succeeded", "timestamp": "2025-12-22T14:54:06"},
    ]
