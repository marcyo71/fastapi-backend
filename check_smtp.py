import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

# Configura i tuoi parametri
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def main():
    try:
        # Crea un messaggio semplice
        msg = MIMEText("Questa è una mail di prova inviata direttamente via SMTP.")
        msg["Subject"] = "SMTP Test"
        msg["From"] = SMTP_USER
        msg["To"] = SMTP_USER  # la mandi a te stesso

        # Connessione al server Gmail
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()  # avvia TLS
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        print("✅ Email inviata con successo, la App Password funziona!")
    except Exception as e:
        print("❌ Errore durante l'invio:", e)

if __name__ == "__main__":
    main()