from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db import Base
import backend.models.user
import backend.models.survey_model
import backend.models.user


# 🔧 Connessione persistente condivisa
engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
connection = engine.connect()
TestingSessionLocal = sessionmaker(bind=connection)

# 🛠️ Crea le tabelle una volta
Base.metadata.create_all(bind=connection)
