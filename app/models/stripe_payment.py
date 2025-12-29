from sqlalchemy import Column, String, Integer
from app.db.base_class import Base

class StripePayment(Base):
    __tablename__ = "stripe_payments"

    session_id = Column(String, primary_key=True, index=True)
    customer_email = Column(String, nullable=True)
    amount_total = Column(Integer, nullable=False)
    payment_status = Column(String, nullable=False)
