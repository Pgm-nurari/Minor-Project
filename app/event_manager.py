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

@event_manager_bp.route('/')
def event_manager():
    return render_template('event_manager/eventmanager_dash.html',events=events, data=transaction_data)

@event_manager_bp.route('/event_details/<int:event_id>')
def event_details(event_id):
    # Get the event based on the ID
    event = next((event for event in events if int(event['id']) == event_id), None)
    if event is None:
        return "Event not found", 404  # Add a 404 error page or message
    return render_template('event_manager/event_details.html', event=event)