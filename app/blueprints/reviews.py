from flask import Blueprint, jsonify, current_app

from app import db
from app.base_view import BaseView
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_kwargs
from app.schemas import ReviewSchema
from app.models import Review

reviews_bp = Blueprint('reviews', __name__, url_prefix=current_app.config['REVIEWS_PREFIX'])


class ReviewView(BaseView):
    """Handler for /users/ endpoint"""
    _endpoint_name = '/'
    _name = 'review'
    decorators = [jwt_required()]

    def get(self):
        """Review view
            ---
            description: Get a review for user
            security:
            - jwt: []
            responses:
              200:
                content:
                  application/json:
                    schema: ReviewSchema
        """
        user_id = get_jwt_identity()
        reviews = Review.query.filter(Review.user_id == user_id).all()
        schema = ReviewSchema(many=True)
        return jsonify(schema.dump(reviews))

    @use_kwargs(ReviewSchema())
    def post(self, **kwargs):
        user_id = get_jwt_identity()
        review = Review(**kwargs, user_id=user_id)
        db.session.add(review)
        db.session.commit()
        return jsonify({'msg': 'OK'}), 201

    def put(self, user_id):
        if user_id is None:
            return {'error': 'user_id not provided'}
        return {'hello': 'put'}

    def delete(self, user_id):
        if user_id is None:
            return {'error': 'user_id not provided'}
        return {'hello': 'delete'}


class ReviewListView(BaseView):
    """Handler for /users endpoint"""
    _endpoint_name = '/list'
    _name = 'reviews'
    decorators = [jwt_required()]

    def get(self):
        """Users view
            ---
            description: Get all users"""
        return jsonify({'data': [{'name': 'Andrii'}, {'name': 'Lena'}]}), 200

