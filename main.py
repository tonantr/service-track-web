import os
from app.app import app
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":

    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "False") == "True"

    app.run(host=host, port=port, debug=debug)
