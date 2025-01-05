from flask import Flask
from .short import short


def register_blueprints(app: Flask):
    """
    Register all blueprints with the Flask application.
    Args:
        app (Flask): The Flask application instance to register blueprints with.
    """

    app.register_blueprint(short)
