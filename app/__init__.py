from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()
login_manager = LoginManager()


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    with app.app_context():
        from .auth.auth import auth
        from .errors.errors import error_403, error_404, error_500

        # Application buleprints
        app.register_blueprint(auth)

        # Error Pages
        app.register_error_handler(404, error_404)
        app.register_error_handler(403, error_403)
        app.register_error_handler(500, error_500)

    return app
