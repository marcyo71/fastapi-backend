from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # Campo database_url, mappato alla variabile d'ambiente DATABASE_URL
    database_url: str = Field(..., alias="DATABASE_URL")

    class Config:
        # Carica automaticamente le variabili dal file .env
        env_file = ".env"
        env_file_encoding = "utf-8"
        # Permette di usare sia l'alias (DATABASE_URL) che il nome del campo (database_url)
        populate_by_name = True
