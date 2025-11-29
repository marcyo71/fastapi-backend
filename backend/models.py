from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    status_id = Column(Integer, ForeignKey("user_status.id"))

    status = relationship("UserStatus", back_populates="users")
    transactions = relationship("Transaction", back_populates="user")
    referrals = relationship("Referral", back_populates="user")

class UserStatus(Base):
    __tablename__ = "user_status"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    users = relationship("User", back_populates="status")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime)

    user = relationship("User", back_populates="transactions")

class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    code = Column(String, unique=True)

    user = relationship("User", back_populates="referrals")
