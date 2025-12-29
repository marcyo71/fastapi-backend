from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.config.settings import settings   # 👈 importa l’istanza

api_key_header = APIKeyHeader(name="Authorization")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token scaduto")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token non valido")

def get_current_user(auth_header: str = Security(api_key_header), db: Session = Security(get_db)):
    if not auth_header:
        raise HTTPException(status_code=401, detail="Header Authorization mancante")

    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    else:
        token = auth_header

    payload = decode_access_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Token non valido")

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    return user

