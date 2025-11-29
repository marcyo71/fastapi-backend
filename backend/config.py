

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    app_env: str = "development"
    debug: bool = True
    api_host: str = "http://127.0.0.1:8000"

    class Config:
        env_file = ".env"

settings = Settings()
