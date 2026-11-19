"""
Gesaivan Market Management System
Application factory and core configuration.
"""
from flask import Flask
from .extensions import mongo
from .config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialise extensions
    mongo.init_app(app)

    # Register blueprints
    from .routes.main import main_bp
    from .routes.buyers import buyers_bp
    from .routes.farmers import farmers_bp
    from .routes.markets import markets_bp
    from .routes.price_listings import price_listings_bp
    from .routes.records import records_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(buyers_bp, url_prefix="/buyers")
    app.register_blueprint(farmers_bp, url_prefix="/farmers")
    app.register_blueprint(markets_bp, url_prefix="/markets")
    app.register_blueprint(price_listings_bp, url_prefix="/price-listings")
    app.register_blueprint(records_bp, url_prefix="/records")

    # Custom error handlers
    from .routes.errors import register_error_handlers
    register_error_handlers(app)

    return app
