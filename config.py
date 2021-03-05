import os

from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(BASEDIR, 'db.sqlite'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMINS = ['your-email@example.com']
    POSTS_PER_PAGE = 5
    LANGUAGES = ['en', 'cz']

    API_V1 = 'v1'
    ROUTES_PREFIX = '/api'
    AUTH_PREFIX = f'{ROUTES_PREFIX}/{API_V1}/auth'
    USERS_PREFIX = f'{ROUTES_PREFIX}/{API_V1}/users'
    REVIEWS_PREFIX = f'{ROUTES_PREFIX}/{API_V1}/reviews'
