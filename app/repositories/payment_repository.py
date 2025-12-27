from sqlalchemy.orm import Session
from app.models.payment import Payment
from app.schemas.payment_schema import PaymentCreate


class PaymentRepository:

    @staticmethod
    def create(db: Session, data: PaymentCreate):
        payment = Payment(**data.dict())
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment

    @staticmethod
    def get_by_session_id(db: Session, session_id: str):
        return db.query(Payment).filter(Payment.session_id == session_id).first()

    @staticmethod
    def update_status(db: Session, session_id: str, status: str):
        payment = PaymentRepository.get_by_session_id(db, session_id)
        if payment:
            payment.status = status
            db.commit()
            db.refresh(payment)
        return payment

    @staticmethod
    def list_payments(db: Session, method: str | None, status: str | None):
        query = db.query(Payment)

        if method:
            query = query.filter(Payment.method == method)

        if status:
            query = query.filter(Payment.status == status)

        return query.order_by(Payment.id.desc()).all()

    @staticmethod
    def total_amount(db: Session, method: str | None, status: str | None):
        query = db.query(Payment)

        if method:
            query = query.filter(Payment.method == method)

        if status:
            query = query.filter(Payment.status == status)

        payments = query.all()
        return sum(p.amount for p in payments)


