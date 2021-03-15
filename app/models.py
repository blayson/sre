from datetime import datetime, timedelta

from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token

from app import DB
from app.exceptions import WrongPassword


class User(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(64), index=True)
    email = DB.Column(DB.String(120), index=True, unique=True, nullable=False)
    password = DB.Column(DB.String(128), nullable=False)
    about_me = DB.Column(DB.String(240))
    last_seen = DB.Column(DB.DateTime, default=datetime.utcnow)
    reviews = DB.relationship('Review', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def __init__(self, **kwargs):
        self.email = kwargs.get('email')
        self.password = bcrypt.hash(kwargs.get('password'))

    def set_password(self, password):
        self.password = bcrypt.hash(password)

    def get_token(self, expire_time=24):
        expire_delta = timedelta(expire_time)
        token = create_access_token(identity=self.id, expires_delta=expire_delta)
        return token

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter(cls.email == email).one()
        if not bcrypt.verify(password, user.password):
            raise WrongPassword('No user with this password')
        return user


class Review(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    changed = DB.Column(DB.Boolean)
    user_id = DB.Column(DB.Integer, DB.ForeignKey('user.id'), nullable=False)
