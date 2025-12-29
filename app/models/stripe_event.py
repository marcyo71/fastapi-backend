from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.base_class import Base

class StripeEvent(Base):
    __tablename__ = "stripe_events"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
