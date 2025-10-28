from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    api_env: str = os.getenv("API_ENV", "development")
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:8080").split(",")

    jwt_secret: str = os.getenv("JWT_SECRET", "devsecret")
    jwt_alg: str = os.getenv("JWT_ALG", "HS256")
    jwt_access_ttl_min: int = int(os.getenv("JWT_ACCESS_TTL_MIN", "15"))
    jwt_refresh_ttl_days: int = int(os.getenv("JWT_REFRESH_TTL_DAYS", "7"))

    argon2_time_cost: int = int(os.getenv("ARGON2_TIME_COST", "2"))
    argon2_memory_cost: int = int(os.getenv("ARGON2_MEMORY_COST", "51200"))
    argon2_parallelism: int = int(os.getenv("ARGON2_PARALLELISM", "2"))

    totp_optional: bool = os.getenv("TOTP_OPTIONAL", "1") == "1"

    db_driver: str = os.getenv("DB_DRIVER", "postgres")
    postgres_user: str = os.getenv("POSTGRES_USER", "budgeteer")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "budgeteer")
    postgres_db: str = os.getenv("POSTGRES_DB", "budgeteer")
    postgres_host: str = os.getenv("POSTGRES_HOST", "db")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    sqlite_path: str = os.getenv("SQLITE_PATH", "/data/budgeteer.db")

    media_root: str = os.getenv("MEDIA_ROOT", "/app/app/media")
    seed_demo: bool = os.getenv("SEED_DEMO", "0") == "1"

    backup_dir: str = os.getenv("BACKUP_DIR", "/backups")

    @property
    def database_url(self) -> str:
        if self.db_driver == "sqlite":
            return f"sqlite:///{self.sqlite_path}"
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

settings = Settings()
