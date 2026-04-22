"""
Flask Application Factory
Author: Akash

Uses hardcoded in-memory data — no MongoDB or MQTT required.
"""

from flask import Flask
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

from .config import Config
from .extensions import jwt


def create_app(config_class=Config):
    """Create Flask application using the app factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    if app.config.get("ENV") == "production":
        if app.config.get("ALLOW_DEMO_LOGIN"):
            raise RuntimeError("ALLOW_DEMO_LOGIN must be disabled in production")
        if app.config.get("SECRET_KEY", "").startswith("dev-secret"):
            raise RuntimeError("SECRET_KEY must be set to a strong value in production")
        if app.config.get("JWT_SECRET_KEY", "").startswith("jwt-secret-change"):
            raise RuntimeError("JWT_SECRET_KEY must be set to a strong value in production")
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", ["http://localhost:3000"])}})
    jwt.init_app(app)
    
    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.cattle import cattle_bp
    from .routes.sensors import sensors_bp
    from .routes.health import health_bp
    from .routes.insurance import insurance_bp
    from .routes.identify import identify_bp
    from .routes.dashboard import dashboard_bp
    from .routes.admin import admin_bp
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(cattle_bp, url_prefix="/api/cattle")
    app.register_blueprint(sensors_bp, url_prefix="/api/sensors")
    app.register_blueprint(health_bp, url_prefix="/api/health")
    app.register_blueprint(insurance_bp, url_prefix="/api/insurance")
    app.register_blueprint(identify_bp, url_prefix="/api/identify")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    
    # Health check
    @app.route("/api/health-check")
    def health_check():
        return {"status": "ok", "service": "cattle-monitoring-api"}

    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        return {
            "error": err.name,
            "message": err.description,
            "status": err.code,
        }, err.code

    @app.errorhandler(Exception)
    def handle_exception(_err):
        return {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status": 500,
        }, 500
    
    return app
