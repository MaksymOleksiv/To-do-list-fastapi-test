from pydantic_settings import BaseSettings
from pydantic import ConfigDict, EmailStr
import enum


class Settings(BaseSettings):
    PROJECT_NAME: str = "To-Do List API"

    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "todo_db"
    POSTGRES_SERVER: str = "db"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    @property
    def CELERY_BROKER_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    @property
    def CELERY_RESULT_BACKEND(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str = "ToDo Planner"

    ADMIN_EMAIL: EmailStr

    model_config = ConfigDict(env_file=".env")


settings = Settings()


class StatusEnum(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
