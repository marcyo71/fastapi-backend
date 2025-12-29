import stripe
from typing import Optional
from sqlalchemy.orm import Session

from app.db.session import AsyncSessionLocal
from app.repositories.payment_repository import PaymentRepository
from app.schemas.payment_schema import PaymentCreate
from app.config.settings import settings

# ============================================================
#   CONFIGURAZIONE STRIPE
# ============================================================
stripe.api_key = settings.stripe_secret_key


class PaymentService:

    # ============================================================
    #   UTILITY DB
    # ============================================================
    @staticmethod
    def get_db() -> Session:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # ============================================================
    #   VALIDAZIONE IMPORTI
    # ============================================================
    @staticmethod
    def validate_amount(amount: Optional[int]):
        if amount is None or amount <= 0:
            raise ValueError("Importo non valido")
        return amount

    # ============================================================
    #   STRIPE CHECKOUT
    # ============================================================
    @staticmethod
    def create_stripe_session(amount: int):
        amount = PaymentService.validate_amount(amount)

        session = stripe.checkout.Session.create(
            mode="payment",
            payment_method_types=["card"],
            line_items=[{
                "price": "price_1STICPDzgrGjJrwILIDv4cJI",
                "quantity": 1
            }],
            success_url="http://localhost:5173/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:5173/cancel",
        )

        # Salvataggio nel DB
        PaymentService.save_payment(
            session_id=session.id,
            amount=amount,
            method="stripe",
            status="pending"
        )

        return session

    # ============================================================
    #   KLARNA CHECKOUT
    # ============================================================
    @staticmethod
    def create_klarna_session(amount: int):
        amount = PaymentService.validate_amount(amount)

        response = {
            "redirect_url": "https://pay.klarna.com/some-session-id"
        }

        PaymentService.save_payment(
            session_id="klarna-session-id",
            amount=amount,
            method="klarna",
            status="pending"
        )

        return response

    # ============================================================
    #   GOOGLE PAY CHECKOUT
    # ============================================================
    @staticmethod
    def create_google_pay_session(amount: int):
        amount = PaymentService.validate_amount(amount)

        response = {
            "redirect_url": "https://pay.google.com/gp/p/ui/pay?session=demo-session-id"
        }

        PaymentService.save_payment(
            session_id="googlepay-session-id",
            amount=amount,
            method="google_pay",
            status="pending"
        )

        return response

    # ============================================================
    #   AGGIORNAMENTO STATO PAGAMENTO (WEBHOOK)
    # ============================================================
    @staticmethod
    def update_payment_status(session_id: str, status: str):
        db = next(PaymentService.get_db())
        return PaymentRepository.update_status(db, session_id, status)

    # ============================================================
    #   METODI DB
    # ============================================================
    @staticmethod
    def save_payment(session_id: str, amount: int, method: str, status: str):
        db = next(PaymentService.get_db())

        data = PaymentCreate(
            session_id=session.id,
            amount=amount,
            method=method,
            status=status
        )

        return PaymentRepository.create(db, data)

    @staticmethod
    def get_payment_by_session_id(session_id: str):
        db = next(PaymentService.get_db())
        return PaymentRepository.get_by_session_id(db, session_id)

    # ============================================================
    #   LISTA PAGAMENTI
    # ============================================================
    @staticmethod
    def list_payments(method: str | None = None, status: str | None = None):
        db = next(PaymentService.get_db())
        return PaymentRepository.list_payments(db, method, status)

    # ============================================================
    #   TOTALE INCASSATO
    # ============================================================
    @staticmethod
    def total_amount(method: str | None = None, status: str | None = None):
        db = next(PaymentService.get_db())
        return PaymentRepository.total_amount(db, method, status)

