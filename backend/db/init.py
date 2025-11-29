from backend.db.database import Base, engine

# importa i modelli per registrare le tabelle
from backend.models.user import User
from backend.models.referral import Referral
from backend.models.transaction import Transaction

def init_db():
    print("🔄 Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Dropped.")

    print("🛠️ Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized.")
