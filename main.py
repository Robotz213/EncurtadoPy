import os
import dotenv

from app import app

"""
This script initializes and runs a Flask web application.

Modules:
    os: Provides a way of using operating system dependent functionality.
    dotenv: Loads environment variables from a .env file.
    app: The Flask application instance.

Functions:
    main: Loads environment variables, sets the debug mode, and runs the Flask app.

Environment Variables:
    DEBUG: Determines if the Flask app should run in debug mode. Expected values are "true", "1", "t", "y", "yes" (case insensitive).

Usage:
    Run this script directly to start the Flask web application on port 8080.
"""


dotenv.load_dotenv()

if __name__ == "__main__":

    debug = os.getenv("DEBUG").lower() in ("true", "1", "t", "y", "yes")
    app.run(port=8080, debug=debug)
