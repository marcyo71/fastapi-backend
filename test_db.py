import sys, os
# Aggiungo la cartella fastapi al path
sys.path.append(os.path.join(os.path.dirname(__file__), "fastapi"))

from models import Base, User, Transaction, Referral
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connessione al tuo DB Postgres (aggiorna password/host se diverso)
DATABASE_URL = "postgresql://marcy:nuovapassword@localhost:5432/fastapi_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def test_db():
    session = SessionLocal()

    # 1. Crea un utente
    marcello = User(name="Marcello", email="marcy@example.com")
    session.add(marcello)
    session.commit()
    session.refresh(marcello)

    # 2. Referral collegato
    referral = Referral(code="ABC123", user_id=marcello.id)
    session.add(referral)

    # 3. Transazione collegata
    transaction = Transaction(amount=99.99, description="Test payment", user_id=marcello.id)
    session.add(transaction)

    session.commit()

    # 4. Stampa i dati
    print("Users:", session.query(User).all())
    print("Referrals:", session.query(Referral).all())
    print("Transactions:", session.query(Transaction).all())

    session.close()

if __name__ == "__main__":
    test_db()
