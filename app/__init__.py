from flask import Flask


def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    with app.app_context():
        pass

    return app
