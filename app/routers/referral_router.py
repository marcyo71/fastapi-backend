from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.referral_schema import ReferralCreate, ReferralRead
from app.services.referral_service import ReferralService

router = APIRouter(prefix="/referrals", tags=["Referrals"])


@router.post("/", response_model=ReferralRead)
async def create_referral(data: ReferralCreate, db: AsyncSession = Depends(get_db)):
    return await ReferralService.create(db, data)


@router.get("/{referral_id}", response_model=ReferralRead)
async def get_referral(referral_id: int, db: AsyncSession = Depends(get_db)):
    referral = await ReferralService.get(db, referral_id)
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")
    return referral


@router.get("/", response_model=list[ReferralRead])
async def get_all_referrals(db: AsyncSession = Depends(get_db)):
    return await ReferralService.get_all(db)

