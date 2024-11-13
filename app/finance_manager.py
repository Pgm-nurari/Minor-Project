from flask import render_template,Blueprint

finance_manager_bp = Blueprint('finance_manager', __name__, url_prefix='/finmng')

users = [{
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


@finance_manager_bp.route('/finance_manager/<int:user_id>')
def finance_manager(user_id):
    # Logic for finance manager, based on user_id
    return render_template('finance_manager/financemanager_dashboard.html', events=events, user=users)

@finance_manager_bp.route('/event_details/<int:event_id>')
def event_details(event_id):
    # Get the event based on the ID
    event = next((event for event in events if int(event['id']) == event_id), None)
    if event is None:
        return "Event not found", 404  # Add a 404 error page or message
    return render_template('finance_manager/event_details.html', event=event)