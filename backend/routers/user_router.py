from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.dependencies import get_db
from backend.models.user import User

user_router = APIRouter(prefix="/users", tags=["users"])

# Endpoint: lista utenti
@user_router.get("/")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]

# Endpoint: crea utente
@user_router.post("/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    # Controllo se esiste già
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email già registrata")

    new_user = User(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "name": new_user.name, "email": new_user.email}
