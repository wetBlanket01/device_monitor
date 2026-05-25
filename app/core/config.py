import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

    model_config = SettingsConfigDict(
        env_file=f"{BASE_DIR}/.env", env_file_encoding="utf-8", extra="ignore"
    )

    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    # Database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str = 'HS256'

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def sync_database_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
