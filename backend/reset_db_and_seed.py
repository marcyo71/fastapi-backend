from backend.db.engine import engine
from backend.db.engine import Base
from backend.seed_db import seed
import backend.models  # 👈 importa tutto centralmente

def reset_db():
    print("🧨 Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Dropped.")

    print("🛠️ Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Created.")

    print("🌱 Seeding database...")
    seed()
    print("🎉 Tutto pronto!")

if __name__ == "__main__":
    reset_db()
