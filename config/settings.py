from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    db_password: Optional[str] = None  # حل مشكلة المتغير الإضافي

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # App
    APP_NAME: str = "بيت الطباعة والألوان"
    SECRET_KEY: str
    DEBUG: bool = False

    # Storage
    UPLOAD_DIR: str = "static/uploads"
    MAX_FILE_SIZE: int = 5 * 1024 * 1024  # 5MB

    # Pydantic v2 Configuration
    model_config = {
        "env_file": ".env",
        "extra": "ignore"  # تجاهل أي متغيرات غير مسجلة لمنع الانهيار
    }

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()