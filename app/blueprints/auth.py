from flask import Blueprint, jsonify, request, current_app
from webargs.flaskparser import use_kwargs

from app.base_view import BaseView
from app.exceptions import WrongPassword
from app.models import User
from app import db, LOGGER
from app.schemas import UserSchema, RegisterSchema, AuthSchema


auth_bp = Blueprint('auth', __name__, url_prefix=current_app.config['AUTH_PREFIX'])


class RegisterView(BaseView):
    """Handler for /auth/register endpoint"""
    _endpoint_name = '/register'
    _name = 'register'

    @use_kwargs(UserSchema(only=('email', 'password'), partial=True))
    def post(self, **kwargs):
        """Register endpoint
            ---
            description: Register user
            parameters:
              in: User
            responses:
              200:
                content:
                  application/json:
                    schema: Auth
        """
        try:
            user = User(**kwargs)
            db.session.add(user)
            db.session.commit()
            token = user.get_token()
            schema = AuthSchema()
        except Exception as e:
            LOGGER.info('User already exists')
            return {'msg': 'user already exists'}, 400
        return jsonify(schema.dump({'token': token}))


class LoginView(BaseView):
    _endpoint_name = '/login'
    _name = 'login'

    @use_kwargs(UserSchema(only=('email', 'password'), partial=True))
    def post(self, **kwargs):
        """Login endpoint
            ---
            description: Login user
            request:
                schema: User
            responses:
              200:
                content:
                  application/json:
                    schema: Auth
        """
        try:
            user = User.authenticate(**kwargs)
            token = user.get_token()
        except TypeError:
            return {'msg': 'missing 2 required parameters'}, 400
        except WrongPassword:
            return {'msg': 'No user with this password'}, 404
        schema = AuthSchema()
        return jsonify(schema.dump({'token': token}))



