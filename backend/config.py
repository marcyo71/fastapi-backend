

# backend/config.py
import os

try:
    # Pydantic v2 con pydantic-settings installato
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback per Pydantic v1
    from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Backend SaaS Marcy/Copilot"
    debug: bool = True
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    secret_key: str = os.getenv("SECRET_KEY", "supersegreto")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    port: int = 8000

    class Config:
        # Compatibilità con Pydantic v1
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"  


# Istanza globale
settings = Settings()
