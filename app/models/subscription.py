from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func
from app.db.base_class import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    # ID della subscription Stripe (es. sub_123)
    id = Column(String, primary_key=True, index=True)

    # ID del customer Stripe (es. cus_123)
    customer_id = Column(String, index=True)

    # Email dell'utente
    email = Column(String, index=True)

    # Stato della subscription (active, canceled, incomplete, trialing, ecc.)
    status = Column(String, index=True)

    # Data di fine periodo corrente (rinnovo)
    current_period_end = Column(DateTime(timezone=True))

    # Timestamp creazione e aggiornamento
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
