from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.dependencies import get_db
from backend.models.user import User
from backend.models.transaction import Transaction

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "balance": u.balance} for u in users]

@router.get("/transactions")
def list_transactions(db: Session = Depends(get_db)):
    txs = db.query(Transaction).order_by(Transaction.timestamp.desc()).all()
    return [
        {
            "id": tx.id,
            "user_id": tx.user_id,
            "amount": tx.amount,
            "timestamp": tx.timestamp.isoformat()
        }
        for tx in txs
    ]
