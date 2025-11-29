from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"   # opzionale, se vuoi usare un file .env
        env_prefix = ""     # nessun prefisso, legge direttamente DATABASE_URL

settings = Settings()
