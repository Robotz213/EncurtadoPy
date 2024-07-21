from app import app
import dotenv
import os
dotenv.load_dotenv()

if __name__ == "__main__":
    
    debug = os.getenv("DEBUG").lower() in ("true", "1", "t", "y", "yes")
    app.run(port = 8080, debug = debug, host = "0.0.0.0")
    