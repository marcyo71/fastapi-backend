from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.backend.db.engine import SessionLocal
from app.backend.models import User

# Istanza del router
user_router = APIRouter(prefix="/users", tags=["users"])

# Dependency per ottenere la sessione DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint: lista utenti
@user_router.get("/")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Endpoint: crea utente
@user_router.post("/")
def create_user(name: str, db: Session = Depends(get_db)):
    new_user = User(name=name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
