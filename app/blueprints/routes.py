from flask import Blueprint, jsonify, current_app

from app.blueprints.users import UserView, UserListView, users_bp, UserReviewsView
from app.blueprints.auth import RegisterView, LoginView, auth_bp
from app.blueprints.reviews import ReviewView, ReviewListView, reviews_bp
from app.base_view import BaseView

routes_bp = Blueprint('routes', __name__, url_prefix=current_app.config['ROUTES_PREFIX'])

# Routes map
BP_VIEWS_MAP = {
    auth_bp: [RegisterView, LoginView],
    users_bp: [UserView, UserListView, UserReviewsView],
    reviews_bp: [ReviewView, ReviewListView]
}


@routes_bp.route('/', methods=['GET'])
def routes():
    endpoints = []
    parse_routes(jsonify_routes_callback, endpoints=endpoints)
    return jsonify(endpoints), 200


def parse_routes(callback, **kwargs):
    for bp, views in BP_VIEWS_MAP.items():
        for view in views:
            callback(view=view, bp=bp, **kwargs)


def route_register_callback(**kwargs):
    view = kwargs.get('view')
    bp = kwargs.get('bp')
    view.register(bp)


def jsonify_routes_callback(**kwargs):
    view: BaseView = kwargs.get('view')
    bp: Blueprint = kwargs.get('bp')
    endpoints = kwargs.get('endpoints')
    endpoints.append(f"{bp.url_prefix}{view._endpoint_name}")


# Register routes and views
parse_routes(route_register_callback)
