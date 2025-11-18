from backend.db.database import SessionLocal
from backend.models.user import User
from backend.models.user import User

def seed_users():
    db = SessionLocal()

    # Pulisce eventuali dati vecchi
    db.query(User).delete()

    # Utente base con ref_code
    alice = User(name="Alice", email="alice@test.com", balance=50.0, ref_code="ALICE123")
    bob = User(name="Bob", email="bob@test.com", balance=20.0, ref_code="BOB123", ref_by="ALICE123")
    carol = User(name="Carol", email="carol@test.com", balance=30.0, ref_code="CAROL123", ref_by="ALICE123")
    dave = User(name="Dave", email="dave@test.com", balance=10.0, ref_code="DAVE123", ref_by="BOB123")

    db.add_all([alice, bob, carol, dave])
    db.commit()
    db.close()
    print("Seed completato: utenti inseriti.")

if __name__ == "__main__":
    seed_users()
