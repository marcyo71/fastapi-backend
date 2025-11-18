from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.models import User, UserStatus, Referral

router = APIRouter()

@router.get("/referrals/{user_id}")
def get_referrals(user_id: int, db: Session = Depends(get_db)):
    # 🔎 Trova l'utente e verifica che sia abbonato
    user = db.query(User).filter(User.id == user_id, User.status == UserStatus.abbonato).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato o non abbonato")

    # 📌 Recupera tutti i referral inviati da questo utente
    referrals = db.query(Referral).filter(Referral.inviter_id == user.id).all()

    # 🔄 Restituisci in JSON
    return {
        "user": user.email,
        "referrals": [
            {
                "id": r.id,
                "invited_id": r.invited_id,
                "created_at": r.created_at.isoformat()
            }
            for r in referrals
        ]
    }
