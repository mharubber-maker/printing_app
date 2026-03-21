from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # App
    APP_NAME: str = "بيت الطباعة والألوان"
    SECRET_KEY: str
    DEBUG: bool = False

    # Storage
    UPLOAD_DIR: str = "static/uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
