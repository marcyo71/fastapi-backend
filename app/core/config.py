import os

class Settings:
    # Ambiente (dev, prod, ecc.)
    env: str = os.getenv("ENV", "dev")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # ✅ DB URLs
    # In locale usi l'URL pubblico di Railway (containers-us-west-...railway.app)
    # In Railway usi l'URL interno (fastapi-db.railway.internal)
    database_url: str = (
        os.getenv("DB_URL_LOCAL")  # URL pubblico per test da WSL
        or os.getenv("DB_URL")     # URL interno per deploy su Railway
    )
    async_database_url: str = os.getenv("DB_URL_ASYNC")

    # ✅ JWT
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # ✅ Stripe
    stripe_secret_key: str = os.getenv("STRIPE_SECRET_KEY")
    stripe_public_key: str = os.getenv("STRIPE_PUBLIC_KEY")
    stripe_webhook_secret: str = os.getenv("STRIPE_WEBHOOK_SECRET")

settings = Settings()