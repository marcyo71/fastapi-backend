from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    status = Column(String, nullable=False, default="free")
    role = Column(String(50), nullable=True)

    referrals = relationship("Referral", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    surveys = relationship("Survey", back_populates="user")
