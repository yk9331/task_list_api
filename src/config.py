import os
from typing import Any, Dict, Optional

from pydantic import validator
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_DATABASE: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any] = {
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 2,
        "pool_timeout": 30,
        "pool_recycle": 1800,
    }

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_uri(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"mysql+pymysql://{values.get('DB_USER')}:{values.get('DB_PASSWORD')}@{values.get('DB_HOST')}:{values.get('DB_PORT')}/{values.get('DB_DATABASE')}"

    class Config:
        env_file = ".env"


class Settings(DBSettings):
    """
    Basic Settings
    """

    ENV: str = "local"


def get_settings() -> Settings:
    configs = {
        "migration": DBSettings,
        "local": Settings,
    }
    return configs.get(os.getenv("ENV", "local"))()


settings = get_settings()
