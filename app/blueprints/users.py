from flask import Blueprint, jsonify, current_app
from marshmallow import fields

from app.base_view import BaseView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Review, User
from app.schemas import ReviewSchema, UserSchema
from webargs.flaskparser import use_kwargs, use_args

users_bp = Blueprint('users', __name__, url_prefix=current_app.config['API_PREFIX'])


class UserView(BaseView):
    """Handler for /users/<int:user_id> endpoint"""
    _endpoint_name = '/users/'
    _name = 'user'
    decorators = [jwt_required()]

    def get(self):
        """User view
            ---
            description: Get a user by id
            security:
            - jwt: []
            responses:
              200:
                content:
                  application/json:
                    schema: User
        """
        user_id = get_jwt_identity()
        user = User.query.filter(User.id == user_id).one()
        schema = UserSchema()
        return jsonify(schema.dump(user))

    # @use_kwargs(UserSchema())
    def post(self):
        return {'hello': 'post'}

    @use_kwargs(UserSchema(partial=True))
    def put(self, user_id):
        if user_id is None:
            return {'error': 'user_id not provided'}
        return {'hello': 'put'}

    def delete(self, user_id):
        if user_id is None:
            return {'error': 'user_id not provided'}
        return {'hello': 'delete'}


class UserListView(BaseView):
    """Handler for /users endpoint"""
    _endpoint_name = '/users/list'
    _name = 'users'
    decorators = [jwt_required()]

    @use_args({"reviews": fields.Boolean(default=False, required=False)}, location="querystring")
    def get(self, args):
        """Users view
            ---
            description: Get all users"""
        users = User.query.all()
        if args.get('reviews', None):
            schema = UserSchema(many=True)
        else:
            schema = UserSchema(many=True, exclude=['reviews'])
        return jsonify(schema.dump(users))


class UserReviewsView(BaseView):
    _endpoint_name = '/users/reviews'
    _name = 'user_reviews'
    decorators = [jwt_required()]

    def get(self):
        """Users view
            ---
            description: Get all users"""
        user_id = get_jwt_identity()
        reviews = Review.query.filter(Review.user_id == user_id).all()
        schema = ReviewSchema(many=True)
        return jsonify(schema.dump(reviews))
