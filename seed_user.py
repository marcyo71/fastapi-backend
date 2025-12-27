# reset_user_password.py
from passlib.context import CryptContext
from app.database import SessionLocal
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def reset_password(email: str, new_password: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print("Utente non trovato")
            return
        user.hashed_password = pwd_context.hash(new_password)
        db.commit()
        print(f"Password aggiornata per {email}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_password("user@example.com", "pippo123")
