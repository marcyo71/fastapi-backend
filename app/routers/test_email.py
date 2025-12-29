from fastapi import APIRouter
from app.utils.email import send_email

router = APIRouter()

@router.get("/send-test-email")
def send_test_email():
    send_email(
        to_address="tuoindirizzo@gmail.com",
        subject="SMTP Test",
        body="Questa è una mail di prova inviata da FastAPI via SMTP."
    )
    return {"message": "✅ Email inviata con successo"}
