from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    amount = Column(Integer, nullable=False)
    method = Column(String, nullable=False)  # stripe, klarna, google_pay
    status = Column(String, nullable=False, default="pending")  # pending, paid, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
