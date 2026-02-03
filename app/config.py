from pydantic_settings import BaseSettings
from typing import Literal

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expiration: int = 15 # minutes
    refresh_token_expiration: int = 7 # days

    deleteUnverifiedUsersInterval: int = 3600 # seconds

    environment: Literal["dev", "prod"] = "dev"

    redis_url: str

    class Config:
        env_file = ".env"

settings = Settings()