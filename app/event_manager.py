from flask import render_template,Blueprint

event_manager_bp = Blueprint('event_manager', __name__, url_prefix='/evemng')

@event_manager_bp.route('/')
def event_manager():
    users = {
        "id" : "1234",
         "username": "John Doe", 
         "email": "john@example.com", 
         "role": "Event Manager",
         "department": "Commerce",
         "event" :  "Annual Conference",
         "phone" : "2136547895",
         "sub_event" : ""
        }
    
    events = [
        {
            "event_name": "Annual Conference",
            "status": "Active",
            "type": "Conference",
            "department": "Marketing",
            "duration": "2 Days"
        },
        {
            "event_name": "Workshop on AI",
            "status": "Upcoming",
            "type": "Workshop",
            "department": "IT",
            "duration": "1 Day"
        },
        {
            "event_name": "Annual Conference",
            "status": "Active",
            "type": "Conference",
            "department": "Marketing",
            "duration": "2 Days"
        },
        {
            "event_name": "Workshop on AI",
            "status": "Upcoming",
            "type": "Workshop",
            "department": "IT",
            "duration": "1 Day"
        },
    ]
    return render_template('event_manager/eventmanager_dash.html',events=events, user=users)