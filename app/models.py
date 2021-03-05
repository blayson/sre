from datetime import datetime, timedelta

from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token

from app import db
from app.exceptions import WrongPassword


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    about_me = db.Column(db.String(240))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='user', lazy=True)

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


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    changed = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
