from flask import render_template,Blueprint
from .test_data import test_event_data, test_user_data

finance_manager_bp = Blueprint('finance_manager', __name__, url_prefix='/finmng')

@finance_manager_bp.route('/finance_manager/<int:user_id>')
def finance_manager(user_id):
    return render_template('finance_manager/financemanager_dashboard.html', events=test_event_data, user=test_user_data)

