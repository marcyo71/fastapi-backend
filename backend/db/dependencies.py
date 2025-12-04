# backend/db/dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database import SessionLocal

# Dependency per DB
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
