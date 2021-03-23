from flask import Blueprint, jsonify, current_app

from app import DB
from app.base_view import BaseView
from flask_jwt_extended import jwt_required, get_jwt_identity
from webargs.flaskparser import use_kwargs
from app.schemas import ReviewSchema
from app.models.models import Reviews

reviews_bp = Blueprint('reviews', __name__, url_prefix=current_app.config['API_PREFIX'])


class ReviewView(BaseView):
    """Handler for /users/ endpoint"""
    _endpoint_name = '/reviews/'
    _name = 'reviewview'
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
        reviews = Reviews.query.filter(Reviews.user_id == user_id).all()
        # schema = ReviewSchema(many=True)
        # return jsonify(schema.dump(reviews))
        return reviews

    @use_kwargs(ReviewSchema())
    def post(self, **kwargs):
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
        review = Reviews(**kwargs, user_id=user_id)
        DB.session.add(review)
        DB.session.commit()
        return jsonify({'message': 'OK'}), 201


class ReviewListView(BaseView):
    """Handler for /users endpoint"""
    _endpoint_name = '/reviews/list'
    _name = 'reviewlistview'
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
        return jsonify({'data': [{'name': 'Andrii'}, {'name': 'Lena'}]}), 200
