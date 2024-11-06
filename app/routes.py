from app import app
from app.home import home_bp
from app.admin import admin_bp
from app.event_manager import event_manager_bp
from app.finance_manager import finance_manager_bp


# Register each Blueprint with the main app
app.register_blueprint(home_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(event_manager_bp)
app.register_blueprint(finance_manager_bp)