from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.config.settings import settings

# Usa la variabile letta da settings
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
