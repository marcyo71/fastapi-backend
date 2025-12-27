from app import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.referral import Referral
from app.models.user import User

router = APIRouter(prefix="/referrals/received", tags=["referrals"])

@router.get("/{user_id}")
def get_received_referrals(user_id: int, db: Session = Depends(get_db)):
    referral = db.query(Referral).filter(Referral.invited_id == user_id).first()
    if not referral:
        return {"user_id": user_id, "invited_by": None}
    
    inviter = db.query(User).filter(User.id == referral.inviter_id).first()
    return {
        "user_id": user_id,
        "invited_by": inviter.email if inviter else None
    }

