import random
from database import SessionLocal
from models import User, UserStatus, Transaction

N_USERS = 10
N_TRANSACTIONS = 30

def get_or_create_status(db, status_name: str):
    obj = db.query(UserStatus).filter_by(status=status_name).first()
    if obj:
        return obj
    obj = UserStatus(status=status_name)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def seed():
    db = SessionLocal()

    # Crea status
    active = get_or_create_status(db, "active")
    premium = get_or_create_status(db, "premium")

    # Crea utenti
    users = []
    for i in range(1, N_USERS + 1):
        email = f"user{i}@example.com"
        existing = db.query(User).filter_by(email=email).first()
        if existing:
            users.append(existing)
        else:
            status_obj = active if i % 2 == 0 else premium
            u = User(name=f"User{i}", email=email, status_id=status_obj.id)
            db.add(u)
            db.commit()
            db.refresh(u)
            users.append(u)

    # Crea transazioni random
    for _ in range(N_TRANSACTIONS):
        user = random.choice(users)
        amount = round(random.uniform(10, 200), 2)
        tx = Transaction(user_id=user.id, amount=amount)
        db.add(tx)

    db.commit()
    print(f"Seed completato: {N_USERS} utenti e {N_TRANSACTIONS} transazioni create.")
    db.close()

if __name__ == "__main__":
    seed()
