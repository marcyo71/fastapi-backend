# seed_admin.py
from passlib.context import CryptContext
from app.database import SessionLocal
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_admin():
    db = SessionLocal()
    try:
        # controlla se esiste già
        existing = db.query(User).filter(User.email == "admin@example.com").first()
        if existing:
            print("Admin già presente")
            return

        hashed_pw = pwd_context.hash("pippo123")  # password in chiaro
        admin = User(
            email="admin@example.com",
            hashed_password=hashed_pw,
            role="admin"
        )
        db.add(admin)
        db.commit()
        print("Admin creato con successo")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
