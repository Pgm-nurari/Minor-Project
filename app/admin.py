from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

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
users = [
    { "id" : "1234",
        "username": "John Doe", 
        "email": "john@example.com", 
        "role": "Event Manager",
        "department": "Commerce",
        "event" :  "Annual Conference",
        "phone" : "2136547895",
        "sub_event" : ""
    },
    {"id" : "1334",
        "username": "Chris Dale", 
        "email": "Chris@example.com", 
        "role": "Event Manager",
        "department": "Computer Science",
        "event" :  "Savishkaara",
        "phone" : "2136547895",
        "sub_event" : "Annual Conference,  Workshop on AI"
    },
    {"id" : "1244",
        "username": "Bharath Krishnan", 
        "email": "BKrishnan@example.com", 
        "role": "Finance Manager",
        "department": "Visual Media",
        "event" :  "Camera Speaks",
        "phone" : "2136547895",
        "sub_event" : ""
    },
]

@admin_bp.route('/')
def admin_dashboard():
    return render_template('admin/admin_dash.html',events=events, users=users)

@admin_bp.route('/event_details/<int:event_id>')
def event_details(event_id):
    # Get the event based on the ID
    event = next((event for event in events if int(event['id']) == event_id), None)
    if event is None:
        return "Event not found", 404  # Add a 404 error page or message
    return render_template('admin/event_details.html', event=event)

