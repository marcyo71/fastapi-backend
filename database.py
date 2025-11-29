from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Path esplicito al DB in root (evita ambiguità)
SQLALCHEMY_DATABASE_URL = "sqlite:///C:/Users/marcy/fastapi_backend/app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
