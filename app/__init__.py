import os
from importlib import import_module

import dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .misc.gen_seed import generate_id

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


dotenv.load_dotenv()
app = Flask(__name__)

env_vars = {key: os.getenv(key) for key in os.environ}
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f'mysql://{env_vars["DBLogin"]}:{env_vars["DBPassword"]}@{env_vars["DBHost"]}/{env_vars["Database"]}'
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PREFERRED_URL_SCHEME"] = "https"
app.config["SESSION_COOKIE_HTTPONLY"] = False
app.config["SESSION_COOKIE_SECURE"] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
app.secret_key = generate_id()

db = SQLAlchemy(app)
jwt = JWTManager(app)


import_module("app.routes", __package__)
