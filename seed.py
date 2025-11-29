# seed.py
from database import Base, engine, SessionLocal
import models

# Ricrea lo schema (se app.db è stato eliminato)
Base.metadata.create_all(bind=engine)

# Sessione DB
db = SessionLocal()

# --- Inserisci UserStatus ---
status_active = models.UserStatus(status="active")
status_inactive = models.UserStatus(status="inactive")
db.add_all([status_active, status_inactive])
db.commit()

# --- Inserisci Users ---
user1 = models.User(name="Mario Rossi", email="mario@example.com", status_id=status_active.id)
user2 = models.User(name="Luca Bianchi", email="luca@example.com", status_id=status_inactive.id)
db.add_all([user1, user2])
db.commit()

# --- Inserisci Transaction ---
transaction1 = models.Transaction(user_id=user1.id, amount=99.90)
db.add(transaction1)
db.commit()

# --- Inserisci Referral ---
referral1 = models.Referral(referrer_id=user1.id, referred_id=user2.id)
db.add(referral1)
db.commit()

db.close()

print("Seed completato: status, utenti, transazioni e referral inseriti!")
