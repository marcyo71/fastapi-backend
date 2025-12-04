from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from backend.database import Base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)



    # Relazioni
    transactions = relationship("Transaction", back_populates="user")
    referrals = relationship("Referral", back_populates="user")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String(200))
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relazione con User
    user = relationship("User", back_populates="transactions")


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relazione con User
    user = relationship("User", back_populates="referrals")
