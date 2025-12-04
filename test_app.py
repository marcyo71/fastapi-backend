from app import app
from config import settings  # importa la tua configurazione da config.py

app = app(title="Test App")

@app.get("/ping")
def ping():
    return {
        "message": "pong",
        "database_url": settings.database_url,
        "stripe_price_id": settings.stripe_price_id
    }
