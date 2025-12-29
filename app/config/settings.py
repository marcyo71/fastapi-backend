from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    # Environment
    env: str = "dev"

    # Database
    database_url: str

    # Stripe
    stripe_secret_key: str
    stripe_webhook_secret: str
    stripe_public_key: str

    # JWT
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Debug
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent.parent / ".env.dev",
        env_file_encoding="utf-8",
        extra="forbid",
        env_prefix=""  # 🔥 permette STRIPE_SECRET_KEY → stripe_secret_key
    )

settings = Settings()
