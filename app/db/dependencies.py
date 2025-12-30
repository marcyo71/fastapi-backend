from fastapi import Depends, Security, HTTPException
from fastapi.security import APIKeyHeader
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from app.models import User
from app.core.config import settings
from app.db.session import engine, Base, SessionLocal

# Header per autenticazione
api_key_header = APIKeyHeader(name="Authorization")

# ---- DB DEPENDENCY ----
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- SETTINGS DEPENDENCY ----
def get_settings_dependency():
    return settings

# ---- INIT & CLOSE DB (per lifespan in main.py) ----
def init_db():
    # inizializzazione DB (sync)
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)

def close_db():
    # chiusura pulita del DB (sync)
    engine.dispose()

# ---- JWT DECODER ----
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token scaduto")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token non valido")

# ---- CURRENT USER DEPENDENCY ----
def get_current_user(
    auth_header: str = Security(api_key_header),
    db: Session = Depends(get_db)
):
    if not auth_header:
        raise HTTPException(status_code=401, detail="Header Authorization mancante")

    # Supporta sia "Bearer <token>" che token diretto
    token = auth_header.split(" ")[1] if auth_header.startswith("Bearer ") else auth_header

    payload = decode_access_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Token non valido")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    return user