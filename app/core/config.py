from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import os


class Settings(BaseSettings):
    # -------------------------
    # ENVIRONMENT
    # -------------------------
    env: str = "dev"  # dev | prod | test

    # -------------------------
    # DATABASE
    # -------------------------
    database_url: str

    # -------------------------
    # STRIPE
    # -------------------------
    stripe_secret_key: str
    stripe_webhook_secret: str
    stripe_public_key: str

    # -------------------------
    # JWT / AUTH
    # -------------------------
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # -------------------------
    # APP SETTINGS
    # -------------------------
    debug: bool = False

    # -------------------------
    # CONFIG
    # -------------------------
    model_config = SettingsConfigDict(
        env_file=".env",        # placeholder, verrà sovrascritto
        extra="forbid",
        case_sensitive=False
    )

    # -------------------------
    # VALIDAZIONI AUTOMATICHE
    # -------------------------
    @field_validator("debug", mode="before")
    def convert_debug(cls, v):
        if isinstance(v, bool):
            return v
        return str(v).lower() in {"1", "true", "yes", "on"}

    @field_validator("access_token_expire_minutes", mode="before")
    def convert_minutes(cls, v):
        return int(v)


# -------------------------
# CARICAMENTO DINAMICO .env
# -------------------------

def load_settings():
    env = os.getenv("ENV", "dev").lower()

    env_file_map = {
        "dev": ".env.dev",
        "prod": ".env.prod",
        "test": ".env.test",
    }

    env_file = env_file_map.get(env, ".env.dev")

    return Settings(_env_file=env_file)


settings = load_settings()

# -------------------------
# DEBUG PRINTS
# -------------------------
print("USING ENV FILE:", settings.model_config.get("env_file"))
print("DATABASE_URL:", settings.database_url)
