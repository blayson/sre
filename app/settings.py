from pydantic import BaseSettings


class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 8000

    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:docker@localhost:7090/mta"

    VERSION = '0.0.0'
    ALLOWED_HOSTS = ['*']
    API_PREFIX = '/api/v1'
    PROJECT_NAME = 'Semantic results evaluator'

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600 * 24  # set token expires time to 24 hours

    debug = True


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
