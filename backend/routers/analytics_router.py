from app import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.models.user import User
from backend.schemas.user_schema import UserReadMinimal
from backend.models.user import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/referrals", response_model=list[UserReadMinimal])
def get_referrals_ranking(db: Session = Depends(get_db)):
    users = db.query(User).all()
    ranking = []
    for u in users:
        # Conta quanti utenti hanno ref_by uguale al ref_code di questo utente
        referral_count = db.query(User).filter(User.ref_by == u.ref_code).count()
        ranking.append({
            "id": u.id,
            "name": u.name,
            "balance": u.balance,
            "referrals": referral_count
        })
    # Ordina per numero di referral decrescente
    ranking.sort(key=lambda x: x["referrals"], reverse=True)
    return ranking
