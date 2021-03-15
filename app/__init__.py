from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.exc import OperationalError

from app.logger import setup_logger
from config import Config
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


def create_app(config_class=Config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    JWT.init_app(app)
    DB.init_app(app)
    MIGRATE.init_app(app, DB)

    with app.test_request_context():
        from .blueprints.routes import routes_bp
        from .blueprints.swagger import swagger_ui_blueprint, SWAGGER_URL
        from .blueprints.users import users_bp
        from .blueprints.auth import auth_bp
        from .blueprints.reviews import reviews_bp

        app.url_map.strict_slashes = False

        app.register_blueprint(routes_bp)
        app.register_blueprint(users_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(reviews_bp)
        app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

        # register all swagger documented functions here
        for fn_name in app.view_functions:
            if fn_name == 'static':
                continue
            # print(f"Loading swagger docs for function: {fn_name}")
            view_fn = app.view_functions[fn_name]
            spec.path(view=view_fn)

        # DB.create_all()

    @app.route("/api/swagger.json")
    def create_swagger_spec():
        return jsonify(spec.to_dict())

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        DB.session.remove()

    # @app.before_request
    # def _db_connect():
    #     try:
    #         DB.make_connector()
    #     except OperationalError:
    #         LOGGER.exception("Error occurred while connecting to database. %s", format_exc())
    #         abort(503, "DB is not running")
    #
    return app


# Move import to the end of file to avoid circular import
from app import models
