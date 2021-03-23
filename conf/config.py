import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '../.env'))

DB_NAME = os.getenv('POSTGRES_DATABASE', "mta").strip()
DB_USER = os.getenv('POSTGRES_USER', "postgres").strip()
DB_PASS = os.getenv('POSTGRES_PASSWORD', "docker").strip()
DB_HOST = os.getenv('POSTGRES_HOST', "localhost").strip()
DB_PORT = int(os.getenv('POSTGRES_PORT', "7090").strip())


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_VERSION = 1
    API_PREFIX = f'/api/v{API_VERSION}'

    # Flask Settings
    DEBUG = False
    TESTING = False

    CORS_ALLOWED_ORIGINS = ['*']


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    DEBUG = True
    TESTING = True
