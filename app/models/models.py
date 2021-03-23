from datetime import timedelta, datetime, timezone

from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token

from app import DB
from app.exceptions import WrongPassword


class Users(DB.Model):
    __table__ = DB.Model.metadata.tables['users']

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))
        self.name = kwargs.get('name')
        self.registered = datetime.now(timezone.utc)
        self.user_roles_id = 1

    def set_password(self, password):
        self.password = bcrypt.hash(password)

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.users_id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise WrongPassword('No user with this password')
        return user


class UserRoles(DB.Model):
    __table__ = DB.Model.metadata.tables['reviews']


class Reviews(DB.Model):
    __table__ = DB.Model.metadata.tables['reviews']

