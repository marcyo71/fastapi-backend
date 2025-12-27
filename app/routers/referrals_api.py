from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app import models

router = APIRouter(prefix="/referrals", tags=["referrals"])

class ReferralCreate(BaseModel):
    user_id: int
    code: str
    referred_email: EmailStr

class ReferralResponse(BaseModel):
    id: int
    user_id: int
    code: str
    referred_email: EmailStr

    class Config:
        from_attributes = True

@router.post("/", response_model=ReferralResponse)
def create_referral(referral: ReferralCreate, db: Session = Depends(get_db)):
    db_referral = models.Referral(**referral.dict())
    db.add(db_referral)
    db.commit()
    db.refresh(db_referral)
    return db_referral

@router.get("/", response_model=list[ReferralResponse])
def list_referrals(db: Session = Depends(get_db)):
    return db.query(models.Referral).all()

@router.get("/{referral_id}", response_model=ReferralResponse)
def read_referral(referral_id: int, db: Session = Depends(get_db)):
    referral = db.query(models.Referral).filter(models.Referral.id == referral_id).first()
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")
    return referral

@router.delete("/{referral_id}")
def delete_referral(referral_id: int, db: Session = Depends(get_db)):
    referral = db.query(models.Referral).filter(models.Referral.id == referral_id).first()
    if not referral:
        raise HTTPException(status_code=404, detail="Referral not found")
    db.delete(referral)
    db.commit()
    return {"detail": "Referral deleted"}
