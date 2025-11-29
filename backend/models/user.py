import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from backend.db.engine import Base

class UserStatus(enum.Enum):
    abbonato = "abbonato"
    attivo = "attivo"
    sospeso = "sospeso"
    free = "free"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    status = Column(Enum(UserStatus), nullable=False)

    transactions = relationship("Transaction", back_populates="user")
