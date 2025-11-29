# 📁 Crea struttura cartelle
New-Item -ItemType Directory -Path "backend\db" -Force
New-Item -ItemType Directory -Path "backend\models" -Force
New-Item -ItemType Directory -Path "backend\routers" -Force
New-Item -ItemType Directory -Path "backend\schemas" -Force

# 📄 Crea base.py
@"
from sqlalchemy.orm import declarative_base

Base = declarative_base()
"@ | Set-Content "backend\db\base.py"

# 📄 Crea database.py
@"
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.base import Base

DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)
"@ | Set-Content "backend\db\database.py"

# 📄 Crea seed.py
@"
from backend.db.database import SessionLocal, create_tables
from backend.models.user_model import User
from backend.models.survey_model import Survey

create_tables()
db = SessionLocal()

users = [
    User(name="Alice", email="alice@example.com", ref_code="alice123"),
    User(name="Bob", email="bob@example.com", ref_code="bob456", ref_by="alice123"),
    User(name="Charlie", email="charlie@example.com", ref_code="charlie789"),
]

surveys = [
    Survey(title="Sondaggio sulla soddisfazione clienti"),
    Survey(title="Sondaggio sul prodotto X"),
    Survey(title="Sondaggio sul servizio Y"),
]

db.add_all(users + surveys)
db.commit()
db.close()

print("✅ Seed completato: utenti e sondaggi inseriti.")
"@ | Set-Content "backend\db\seed.py"
