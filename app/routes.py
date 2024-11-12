# app/routes.py

from .home import home_bp
from .admin import admin_bp
from .event_manager import event_manager_bp
from .finance_manager import finance_manager_bp

def register_blueprints(app):
    """Registers all blueprints with the provided app instance."""
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(event_manager_bp)
    app.register_blueprint(finance_manager_bp)
