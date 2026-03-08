"""
Flask Application Factory
Author: Akash

Uses hardcoded in-memory data — no MongoDB or MQTT required.
"""

from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import jwt


def create_app(config_class=Config):
    """Create Flask application using the app factory pattern."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt.init_app(app)
    
    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.cattle import cattle_bp
    from .routes.sensors import sensors_bp
    from .routes.health import health_bp
    from .routes.insurance import insurance_bp
    from .routes.identify import identify_bp
    from .routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(cattle_bp, url_prefix="/api/cattle")
    app.register_blueprint(sensors_bp, url_prefix="/api/sensors")
    app.register_blueprint(health_bp, url_prefix="/api/health")
    app.register_blueprint(insurance_bp, url_prefix="/api/insurance")
    app.register_blueprint(identify_bp, url_prefix="/api/identify")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    
    # Health check
    @app.route("/api/health-check")
    def health_check():
        return {"status": "ok", "service": "cattle-monitoring-api"}
    
    return app
