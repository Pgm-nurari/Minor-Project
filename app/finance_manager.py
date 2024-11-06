from flask import render_template,Blueprint

finance_manager_bp = Blueprint('finance_manager', __name__, url_prefix='/finmng')