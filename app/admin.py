from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_dashboard():
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
    return render_template('admin/admin_dash.html',events=events, users=users)
