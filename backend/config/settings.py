from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # Database
    database_url: str
    database_url_local: str | None = None
    postgres_user: str
    postgres_password: str
    postgres_db: str
    port: int

    # Debug
    debug: bool = False

    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # Stripe
    stripe_secret_key: str
    stripe_public_key: str
    stripe_webhook_secret: str

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
