
from app.blueprints.users import UserView, UserListView, users_bp, UserReviewsView
from app.blueprints.auth import RegisterView, LoginView, auth_bp
from app.blueprints.reviews import ReviewView, ReviewListView, reviews_bp


# Blueprint - view map
BP_VIEWS_MAP = {
    users_bp: (UserView, UserListView, UserReviewsView),
    reviews_bp: (ReviewView, ReviewListView),
    auth_bp: (RegisterView, LoginView),
}


def register_routes():
    for bp, views in BP_VIEWS_MAP.items():
        for view in views:
            view.register(bp)

