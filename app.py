from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/forgot-password")
def forgot_password():
    return render_template("forgotpassword.html")

@app.route("/reset-password")
def reset_password():
    return render_template("resetpassword.html")

@app.route('/admin-dashboard')
def admin():
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
    return render_template('admin_dash.html',events=events, users=users)

@app.route('/event-manager-dashboard')
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
    return render_template('eventmanager_dash.html',events=events, user=users)