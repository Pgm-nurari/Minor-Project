from flask import render_template,Blueprint
from .test_data import test_event_data, test_user_data

event_manager_bp = Blueprint('event_manager', __name__, url_prefix='/evemng')

@event_manager_bp.route('/event_manager/<int:user_id>')
def event_manager(user_id):
    return render_template('event_manager/eventmanager_dash.html',events=test_event_data, data=test_user_data)

