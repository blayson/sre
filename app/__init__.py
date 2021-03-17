from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError

from app.logger import setup_logger
from config import DevelopmentConfig
from app.api_spec import spec

MIGRATE = Migrate()
DB = SQLAlchemy()
JWT = JWTManager()

LOGGER = setup_logger()


# SQLAlchemy
# engine = create_engine(SQLALCHEMY_DATABASE_URI)
# Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# session = scoped_session(Session)
# Base = declarative_base()
# Base.query = session.query_property()


def create_app(config_class=DevelopmentConfig):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    JWT.init_app(app)
    DB.init_app(app)
    MIGRATE.init_app(app, DB)

    with app.test_request_context():
        from app.routes import register_routes
        from .blueprints.swagger import swagger_ui_blueprint, SWAGGER_URL
        from .blueprints.users import users_bp
        from .blueprints.auth import auth_bp
        from .blueprints.reviews import reviews_bp

        app.url_map.strict_slashes = False
        # register routes
        register_routes()

        app.register_blueprint(users_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(reviews_bp)
        app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

        # register all swagger documented functions here
        for fn_name in app.view_functions:
            if fn_name == 'static':
                continue
            view_fn = app.view_functions[fn_name]
            spec.path(view=view_fn)

    @app.route("/api/swagger.json")
    def create_swagger_spec():
        return jsonify(spec.to_dict())

    return app


# Move import to the end of file to avoid circular import
from app import models
