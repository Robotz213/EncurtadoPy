import os

import dotenv

from app import app

dotenv.load_dotenv()

if __name__ == "__main__":

    debug = os.getenv("DEBUG").lower() in ("true", "1", "t", "y", "yes")
    app.run(port=8080, debug=debug)
