import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8000

    database_url = "postgresql://postgres:docker@localhost:7090/mta"

    version = "0.0.1a"
    allowed_hosts = ["*"]
    api_prefix = "/api/v1"
    project_name = "Semantic results evaluator"

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expires_s: int = 3600 * 24 * 31  # set token expires time to 24 hours

    debug = True


uri = os.getenv("DATABASE_URL", "postgresql://postgres:docker@localhost:7090/mta")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)


settings = Settings(
    _env_file=".env",
    _env_file_encoding="utf-8",
)
settings.database_url = uri
