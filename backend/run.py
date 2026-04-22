"""
Entry point — Run the Flask server
Author: Akash
"""

import os

from app import create_app
from app.config import get_config_class

app = create_app(get_config_class())

if __name__ == "__main__":
    debug = os.getenv("FLASK_ENV", "development").lower() != "production"
    app.run(host="0.0.0.0", port=5000, debug=debug)
