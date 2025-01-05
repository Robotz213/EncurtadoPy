"""
This module initializes and configures a Flask application with various extensions,
blueprints, and security features. It includes the following components:

- SQLAlchemy for database interactions
- Flask-Mail for email support
- Flask-Login for user session management
- Flask-Talisman for security headers and HTTPS enforcement
- Logging setup for application logs

The AppFactory class provides methods to initialize these components and create
a Flask application instance with the necessary configurations.

Classes:
    AppFactory: A factory class for creating and configuring a Flask application instance.

Functions:
    create_app: A function to create and configure the Flask application instance.
"""

from datetime import timedelta
from importlib import import_module
from pathlib import Path

from dotenv import dotenv_values
from flask import Flask

# from flask_login import LoginManager
# from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from flask_jwt_extended import JWTManager

# from .logs.setup import initialize_logging

db = SQLAlchemy()
tlsm = Talisman()
jwt = JWTManager()
# mail = Mail()
# login_manager = LoginManager()
# login_manager.login_view = "auth.login"
# login_manager.login_message = "Faça login para acessar essa página."
# login_manager.login_message_category = "info"

objects_config = {
    "development": "app.config.DevelopmentConfig",
    "production": "app.config.ProductionConfig",
    "testing": "app.config.TestingConfig",
}


class AppFactory:
    """
    A factory class for creating and configuring a Flask application instance.
    This class provides methods to initialize extensions, blueprints, and the database
    for a Flask application. It also sets up logging and configures various security
    features.
    Methods:
        init_extensions(app: Flask):
            Initialize Flask extensions such as database, mail, login manager, and security policies.
        create_app() -> Flask:
            Create and configure the Flask application instance with necessary configurations,
            extensions, blueprints, and logging.
        init_blueprints(app: Flask):
        init_database(app: Flask, db: SQLAlchemy):
            Initialize the database for the Flask application, checking for existing initialization
            and ensuring the presence of necessary tables.
    """

    def create_app(self) -> Flask:
        """
        Create and configure the Flask application.
        This function initializes the Flask application with the necessary
        configurations, extensions, blueprints, and logging.
        Returns:
            Flask: The configured Flask application instance.
        """

        src_path = Path(__file__).parent.resolve().joinpath("static")
        app = Flask(__name__, static_folder=src_path)

        env_ambient = dotenv_values(".env")["AMBIENT_CONFIG"]
        ambient = objects_config[env_ambient]

        app.config.from_object(ambient)

        self.init_extensions(app, env_ambient)
        self.init_blueprints(app)

        # """ Initialize logs module """

        # app.logger = initialize_logging()

        return app

    def init_extensions(self, app: Flask, env_ambient: str = "production"):

        db.init_app(app)
        # mail.init_app(app)
        # login_manager.init_app(app)

        jwt.init_app(app)

        csp = app.config["CSP"]
        with app.app_context():

            self.init_database(app, db)

            if env_ambient == "production":
                tlsm.init_app(
                    app,
                    content_security_policy=csp,
                    force_https_permanent=True,
                    force_https=True,
                    session_cookie_http_only=True,
                    session_cookie_samesite="Lax",
                    strict_transport_security_max_age=timedelta(days=31).max.seconds,
                    x_content_type_options=True,
                    x_xss_protection=True,
                )

            import_module(".routes", __package__)

    def init_blueprints(self, app: Flask):
        """
        Initialize and register blueprints with the Flask application.
        This method imports the necessary blueprints from the app.routes module
        and registers them with the provided Flask application instance.
        Args:
            app (Flask): The Flask application instance to register blueprints with.
        """

        from .routes import register_blueprints

        register_blueprints(app)

    def init_database(self, app: Flask, db: SQLAlchemy):
        """
        - Initialize the database for the Flask application.
        This method checks if the database has been initialized by looking for the
        presence of a file named "is_init.txt". If the file does not exist, it calls
        the `init_database` function from `app.models` to initialize the database and
        writes the result to "is_init.txt". Additionally, it checks if the `Users`
        table exists in the database, and if not, it reinitializes the database and
        writes the result to "is_init.txt".

        Args:
            app (Flask): The Flask application instance.
            db (SQLAlchemy): The SQLAlchemy database instance.
        """

        from .models import init_database

        if not Path("is_init.txt").exists():

            with open("is_init.txt", "w") as f:
                f.write(f"{init_database(app, db)}")

        from .models import Users

        if not db.engine.dialect.has_table(db.engine.connect(), Users.__tablename__):
            with open("is_init.txt", "w") as f:
                f.write(f"{init_database(app, db)}")


create_app = AppFactory().create_app
"""
This module initializes the Flask application, configures environment variables,
sets up the SQLAlchemy database connection, and initializes JWT for authentication.

Modules and Packages:
- os: Provides a way of using operating system dependent functionality.
- importlib: Provides the implementation of the import statement.
- dotenv: Loads environment variables from a .env file.
- flask: A micro web framework for Python.
- flask_jwt_extended: Provides JWT support for Flask.
- flask_sqlalchemy: Adds SQLAlchemy support to Flask.
- .misc.gen_seed: Custom module to generate a unique secret key.

Attributes:
- app (Flask): The Flask application instance.
- env_vars (dict): A dictionary containing environment variables.
- db (SQLAlchemy): The SQLAlchemy database instance.
- jwt (JWTManager): The JWT manager instance.

Configuration:
- SQLALCHEMY_DATABASE_URI: The database URI that should be used for the connection.
- SQLALCHEMY_TRACK_MODIFICATIONS: A flag to disable or enable modification tracking.
- PREFERRED_URL_SCHEME: The preferred URL scheme (http or https).
- SESSION_COOKIE_HTTPONLY: A flag to disable or enable HTTPOnly for session cookies.
- SESSION_COOKIE_SECURE: A flag to disable or enable secure cookies.
- JWT_SECRET_KEY: The secret key used to sign JWT tokens.
- secret_key: A unique secret key generated for the application.

Imports:
- app.routes: Imports the routes module to register the application routes.
"""
