"""
Flask App Configuration
Author: Akash
"""

import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the backend directory (where this config.py's package lives)
_backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(_backend_dir / ".env")


class Config:
    """Base configuration."""
    ENV = os.getenv("FLASK_ENV", "development").lower()
    DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me-please-override")
    
    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-change-me-please-use-32-plus-chars")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # Demo compatibility switch (must be false in production)
    ALLOW_DEMO_LOGIN = os.getenv("ALLOW_DEMO_LOGIN", "0") == "1"

    # Comma-separated list, e.g. "https://app.example.com,https://admin.example.com"
    CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if o.strip()]
    
    # File upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "..", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"


def get_config_class():
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "production":
        return ProductionConfig
    return DevelopmentConfig
