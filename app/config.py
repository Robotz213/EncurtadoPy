import secrets
from datetime import timedelta
from pathlib import Path

from dotenv import dotenv_values


class Config(object):
    """
    Configuration class for the application.

    Attributes:
        DEBUG (bool): Enable or disable debug mode.
        TESTING (bool): Enable or disable testing mode.
        SECRET_KEY (str): Secret key for session management.
        JWT_SECRET_KEY (str): Secret key for JWT authentication.

        MAIL_SERVER (str): Mail server address.
        MAIL_PORT (int): Mail server port.
        MAIL_USE_TLS (bool): Enable or disable TLS for mail.
        MAIL_USE_SSL (bool): Enable or disable SSL for mail.
        MAIL_USERNAME (str): Username for mail server authentication.
        MAIL_PASSWORD (str): Password for mail server authentication.
        MAIL_DEFAULT_SENDER (str): Default sender email address.

        SQLALCHEMY_POOL_SIZE (int): Number of connections in the pool.
        SQLALCHEMY_MAX_OVERFLOW (int): Number of extra connections beyond the pool size.
        SQLALCHEMY_POOL_TIMEOUT (int): Timeout for obtaining a connection.
        SQLALCHEMY_POOL_RECYCLE (int): Time (in seconds) to recycle idle connections.
        SQLALCHEMY_POOL_PRE_PING (bool): Check the health of the connection before using it.
        SQLALCHEMY_DATABASE_URI (str): Database URI.
        SQLALCHEMY_ENGINE_OPTIONS (dict): Additional options for SQLAlchemy engine.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Enable or disable modification tracking.

        PREFERRED_URL_SCHEME (str): Preferred URL scheme (http or https).
        SESSION_COOKIE_HTTPONLY (bool): Enable or disable HTTPOnly for session cookies.
        SESSION_COOKIE_SECURE (bool): Enable or disable secure flag for session cookies.
        PERMANENT_SESSION_LIFETIME (int): Lifetime of a permanent session in seconds.

        TEMP_PATH (Path): Path to the temporary directory.

        CSP (dict): Content Security Policy settings.
    """

    DEBUG: bool = False
    TESTING: bool = False
    SECRET_KEY: str = secrets.token_hex(16)
    JWT_SECRET_KEY: str = secrets.token_hex(16)

    # FLASK-MAIL CONFIG
    MAIL_SERVER: str = ""
    MAIL_PORT = 587
    MAIL_USE_TLS: bool = False
    MAIL_USE_SSL: bool = False
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_DEFAULT_SENDER: str = ""

    # SQLALCHEMY CONFIG
    SQLALCHEMY_POOL_SIZE = 30  # Número de conexões na pool
    SQLALCHEMY_MAX_OVERFLOW = 10  # Número de conexões extras além da pool_size
    SQLALCHEMY_POOL_TIMEOUT = 30  # Tempo de espera para obter uma conexão

    # Tempo (em segundos) para reciclar as conexões ociosas
    SQLALCHEMY_POOL_RECYCLE = 1800

    # Verificar a saúde da conexão antes de usá-la
    SQLALCHEMY_POOL_PRE_PING = True

    SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # FLASK CONFIG
    PREFERRED_URL_SCHEME = "https"
    SESSION_COOKIE_HTTPONLY = False
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=31).max.seconds

    TEMP_PATH = Path(__file__).cwd().joinpath("temp")
    TEMP_PATH.mkdir(exist_ok=True)

    CSP = {
        "default-src": ["'self'"],
        "script-src": [
            "'self'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://unpkg.com",
            "https://code.jquery.com",
            "https://use.fontawesome.com",
            "",
            "'unsafe-inline'",
        ],
        "style-src": [
            "'self'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://unpkg.com",
            "https://github.com",
            "https://avatars.githubusercontent.com",
            "'unsafe-inline'",
        ],
        "img-src": [
            "'self'",
            "data:",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://unpkg.com",
            "https://cdn-icons-png.flaticon.com",
            "https://github.com",
            "https://domain.cliente.com",
            "https://avatars.githubusercontent.com",
            "https://cdn-icons-png.freepik.com",
        ],
        "connect-src": [
            "'self'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://cdn.datatables.net",
            "https://github.com",
            "https://unpkg.com",
            "https://avatars.githubusercontent.com",
        ],
        "frame-src": [
            "'self'",
            "https://domain.cliente.com",
            "https://github.com",
            "https://avatars.githubusercontent.com",
        ],
    }


class ProductionConfig(Config):

    try:
        env = dotenv_values(".env")

        # Flask-mail config

        if env.get("MAIL_SERVER"):
            MAIL_SERVER = env["MAIL_SERVER"]
            MAIL_PORT = int(env["MAIL_PORT"])
            MAIL_USE_TLS = env["MAIL_USE_TLS"] in ["True", "true", "TRUE"]
            MAIL_USE_SSL = env["MAIL_USE_SSL"] in ["True", "true", "TRUE"]
            MAIL_USERNAME = env["MAIL_USERNAME"]
            MAIL_PASSWORD = env["MAIL_PASSWORD"]
            MAIL_DEFAULT_SENDER = env["MAIL_DEFAULT_SENDER"]

        # SQLALCHEMY CONFIG

        if env.get("DATABASE_HOST"):
            SQLALCHEMY_DATABASE_URI = "".join(
                [
                    "postgresql+psycopg2://",
                    str(env["DATABASE_USER"]),
                    ":",
                    str(env["DATABASE_PW"]),
                    "@",
                    str(env["DATABASE_HOST"]),
                    ":",
                    str(env["DATABASE_PORT"]),
                    "/",
                    str(env["DATABASE_NAME"]),
                ]
            )

    except Exception as e:
        raise e


class DevelopmentConfig(Config):

    from flask_talisman import DEFAULT_CSP_POLICY

    CSP = DEFAULT_CSP_POLICY
    try:
        env = dotenv_values(".env")

        # Flask-mail config
        if env.get("MAIL_SERVER"):
            MAIL_SERVER = env["MAIL_SERVER"]
            MAIL_PORT = int(env["MAIL_PORT"])
            MAIL_USE_TLS = env["MAIL_USE_TLS"] in ["True", "true", "TRUE"]
            MAIL_USE_SSL = env["MAIL_USE_SSL"] in ["True", "true", "TRUE"]
            MAIL_USERNAME = env["MAIL_USERNAME"]
            MAIL_PASSWORD = env["MAIL_PASSWORD"]
            MAIL_DEFAULT_SENDER = env["MAIL_DEFAULT_SENDER"]

    except Exception as e:
        raise e


class TestingConfig(Config):

    from flask_talisman import DEFAULT_CSP_POLICY

    env = dotenv_values(".env")
    CSP = DEFAULT_CSP_POLICY
    try:
        TESTING = True

        # Flask-mail config
        if env.get("MAIL_SERVER"):
            MAIL_SERVER = env["MAIL_SERVER"]
            MAIL_PORT = int(env["MAIL_PORT"])
            MAIL_USE_TLS = env["MAIL_USE_TLS"] in ["True", "true", "TRUE"]
            MAIL_USE_SSL = env["MAIL_USE_SSL"] in ["True", "true", "TRUE"]
            MAIL_USERNAME = env["MAIL_USERNAME"]
            MAIL_PASSWORD = env["MAIL_PASSWORD"]
            MAIL_DEFAULT_SENDER = env["MAIL_DEFAULT_SENDER"]

    except Exception as e:
        raise e


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = "sqlite:///local.db"
