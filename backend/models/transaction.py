from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.sql import func
from backend.db.engine import Base  # ✅ Assicurati che punti al Base giusto

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    customer_email = Column(String, nullable=True)
    amount_total = Column(Integer)  # in centesimi
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # ✅ Nuovi campi
    amount = Column(Float, nullable=False)
    currency = Column(String, default="EUR")
