from flask import render_template,Blueprint

event_manager_bp = Blueprint('event_manager', __name__, url_prefix='/evemng')

transaction_data = [{
    "id" : "1234",
        "username": "John Doe", 
        "email": "john@example.com", 
        "role": "Event Manager",
        "department": "Commerce",
        "event" :  "Annual Conference",
        "phone" : "2136547895",
        "sub_event" : ""
    }
]
events = [
    {
        "id" : '1234',
        "event_name": "Annual Conference",
        "status": "Active",
        "type": "Conference",
        "department": "Marketing",
        "duration": "2 Days"
    },
    {
        "id" : '1345',
        "event_name": "Workshop on AI",
        "status": "Upcoming",
        "type": "Workshop",
        "department": "IT",
        "duration": "1 Day"
    },
    {
        "id" : '3345',
        "event_name": "Annual Conference",
        "status": "Active",
        "type": "Conference",
        "department": "Marketing",
        "duration": "2 Days"
    },
    {
        "id" : '6545',
        "event_name": "Workshop on AI",
        "status": "Upcoming",
        "type": "Workshop",
        "department": "IT",
        "duration": "1 Day"
    },
]

@event_manager_bp.route('/event_manager/<int:user_id>')
def event_manager(user_id):
    # Logic for event manager, based on user_id
    return render_template('event_manager/eventmanager_dash.html',events=events, data=transaction_data)

