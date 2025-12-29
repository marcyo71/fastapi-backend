from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.utils import get_password_hash
from app.models import User, Base  # ⚠️ Adatta l'import se User/Base sono altrove

DATABASE_URL = "postgresql://marcy:tuapassword@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def seed_user():
    db = SessionLocal()
    try:
        plain_password = "m@rcy2025"
        hashed_password = get_password_hash(plain_password)

        user = User(
            email="marcy@example.com",
            password=hashed_password   # <-- usa 'password'
        )

        db.add(user)
        db.commit()
        print(f"Utente creato: marcy@example.com con password '{plain_password}'")
    finally:
        db.close()

if __name__ == "__main__":
    seed_user()
