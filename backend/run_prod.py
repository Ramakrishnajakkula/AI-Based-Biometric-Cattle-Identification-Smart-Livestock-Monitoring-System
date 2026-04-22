"""Production runner using Waitress.

Usage:
  set FLASK_ENV=production
  python backend/run_prod.py
"""

import os

from waitress import serve

from app import create_app
from app.config import get_config_class


if __name__ == "__main__":
    app = create_app(get_config_class())
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    serve(app, host=host, port=port)
