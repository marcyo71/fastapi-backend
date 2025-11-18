from backend.db.database import SQLALCHEMY_DATABASE_URL
print(f"Sto usando questo DB: {SQLALCHEMY_DATABASE_URL}")

from backend.db.database import SessionLocal
from backend.models.user import User, UserStatus
from backend.models.referral import Referral

def seed():
    db = SessionLocal()

    # Utenti abbonati (inviter)
    abbonato1 = User(email="abbonato1@example.com", name="Mario Rossi", status=UserStatus.abbonato)
    abbonato2 = User(email="abbonato2@example.com", name="Anna Neri", status=UserStatus.abbonato)

    # Utenti free (invited)
    free1 = User(email="free1@example.com", name="Luca Bianchi", status=UserStatus.free)
    free2 = User(email="free2@example.com", name="Giulia Verdi", status=UserStatus.free)
    free3 = User(email="free3@example.com", name="Paolo Gallo", status=UserStatus.free)

    db.add_all([abbonato1, abbonato2, free1, free2, free3])
    db.commit()

    # Referral multipli
    # Mario invita Luca e Giulia
    ref1 = Referral(inviter_id=abbonato1.id, invited_id=free1.id)
    ref2 = Referral(inviter_id=abbonato1.id, invited_id=free2.id)

    # Anna invita Giulia e Paolo
    ref3 = Referral(inviter_id=abbonato2.id, invited_id=free2.id)
    ref4 = Referral(inviter_id=abbonato2.id, invited_id=free3.id)

    db.add_all([ref1, ref2, ref3, ref4])
    db.commit()

    print("✅ Seed completato: creati 2 abbonati e 3 free con referral multipli")

if __name__ == "__main__":
    seed()
