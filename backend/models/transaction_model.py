from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.db.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Importo in EUR (cent)
    amount = Column(Float, nullable=False)

    # Metodo di pagamento (es. "sepa_debit", "card", "paypal")
    method = Column(String, nullable=False)

    # Stato (es. "pending", "succeeded", "failed")
    status = Column(String, default="pending")

    # ID transazione del provider (Stripe, GoCardless, ecc.)
    provider_id = Column(String, unique=True, index=True)

    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
