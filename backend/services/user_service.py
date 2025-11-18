from backend.models.user import User
from sqlalchemy.orm import Session
from backend.models.user import User
from backend.db import Base


def create_user(name: str, email: str, db: Session) -> User:
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()
