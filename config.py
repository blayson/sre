import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

DB_NAME = os.getenv('POSTGRES_DATABASE', "postgres").strip()
DB_USER = os.getenv('POSTGRES_USER', "postgres").strip()
DB_PASS = os.getenv('POSTGRES_PASSWORD', "postgres").strip()
DB_HOST = os.getenv('POSTGRES_HOST', "0.0.0.0").strip()
DB_PORT = int(os.getenv('POSTGRES_PORT', "5432").strip())


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    API_VERSION = 1
    API_PREFIX = f'/api/v{API_VERSION}'
