# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config

# Initialize SQLAlchemy without an app instance here
db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize the db with the app
    db.init_app(app)

    # Register blueprints
    from . import routes
    routes.register_blueprints(app)

    # Import models so they are registered with SQLAlchemy
    with app.app_context():
        from .modules import models  # Importing models registers them with SQLAlchemy
    
    return app


