from app.db.database import SessionLocal, create_tables
from app.models.user import User
from app.models.survey_model import Survey
from app.models.transaction import Transaction
from app.models.user import UserStatus
from app.models.referral import Referral

# 🔁 Crea tabelle e sessione
create_tables()
db = SessionLocal()

# 🧹 Pulisce il database
db.query(Transaction).delete()
db.query(Survey).delete()
db.query(User).delete()
db.commit()

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

# ✅ Funzione per evitare duplicati
def get_or_create_user(db, **kwargs):
    existing = db.query(User).filter_by(email=kwargs["email"]).first()
    if existing:
        return existing
    user = User(**kwargs)
    db.add(user)
    return user

# 👤 Inserisce utenti
alice = get_or_create_user(db, name="Alice", email="alice@example.com", ref_code="alice123")
bob = get_or_create_user(db, name="Bob", email="bob@example.com", ref_code="bob456", ref_by="alice123")
charlie = get_or_create_user(db, name="Charlie", email="charlie@example.com", ref_code="charlie789")

# 📋 Inserisce sondaggi
surveys = [
    Survey(title="Sondaggio sulla soddisfazione clienti", user=alice, reward=1.5),
    Survey(title="Sondaggio sul prodotto X", user=bob, reward=2.0),
    Survey(title="Sondaggio sul servizio Y", user=charlie, reward=1.0),
]

db.add_all(surveys)
db.commit()
db.close()

print("✅ Seed completato: utenti e sondaggi inseriti.")

