from flask import Blueprint, render_template, redirect, request, flash, url_for, get_flashed_messages, session   
from . import db
from .modules.models import Department, Role, User, EventType, Event, SubEvent
from .modules.db_queries import *
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from datetime import datetime, date
from .test_data import test_user_data, test_event_data


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_dashboard():
    # Retrieve all users
    users = filter_data(User)  # Fetch all users

    # Prepare structured data for each user by calling get_user_info for each one
    user_data = [get_user_info(user) for user in users]

    # Render the template with the structured user data
    return render_template('admin/admin_dash.html', data=user_data, users_table = get_user_table_data(), events=get_event_data())

@admin_bp.route('/authorize/<int:user_id>', methods=['POST'])
def authorize_user(user_id):
    """Route to handle user authorization by updating Verified status."""
    try:
        # Find the user by ID
        user = User.query.get(user_id)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('admin.admin_dashboard'))
        
        # Check if the user is already authorized
        if user.Verified == 1:
            flash("User is already authorized.", "info")
            return redirect(url_for('admin.admin_dashboard'))
        
        # Update the Verified status
        user.Verified = 1
        db.session.commit()
        flash("User has been authorized successfully.", "success")
    
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error authorizing user:", e)
        flash("An error occurred while authorizing the user.", "error")
    
    # Redirect back to the dashboard
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/event_details/<int:event_id>')
def event_details(event_id):
    # Fetch the event from the database
    event = Event.query.get(event_id)
    
    if event is None:
        return "Event not found", 404  # Return 404 if event doesn't exist

    # Get the event manager and finance manager, assuming they are linked
    event_manager = event.event_manager if event.event_manager else None
    finance_manager = event.finance_manager if event.finance_manager else None

    # Fetch the related sub-events, if any
    sub_events = SubEvent.query.filter_by(Event_ID=event_id).all()
    
    # Pass all the data to the template
    return render_template('admin/event_details.html', 
                           event=event,
                           event_manager=event_manager,
                           finance_manager=finance_manager,
                           sub_events=sub_events)

@admin_bp.route('/new_user', methods=['POST', 'GET'])
def new_user():
    if request.method == 'POST':
        # Process form data
        username = request.form.get('username')
        department_name = request.form.get('department')
        role_name = request.form.get('role')
        email = request.form.get('email')
        print("Form data:", username, department_name, role_name, email)

        # Fetch department and role from the database
        department = Department.query.filter_by(Dept_ID=department_name).first()
        role = Role.query.filter_by(Role_ID=role_name).first()


        # Check if the department and role exist
        if not department:
            flash('Department not found.', 'error')
            return redirect(url_for('admin.new_user'))

        if not role:
            flash('Role not found.', 'error')
            return redirect(url_for('admin.new_user'))

        # Create a new user
        user_data = {
            'Username': username,
            'Email': email,
            'Role': role.Role_ID,  # Assuming Role_ID is the ID you need
            'Dept_ID': department.Dept_ID,  # Assuming Dept_ID is the ID you need
            'Password': ''  # Setting password as blank
        }

        # Add the new user to the database using the create_entry function
        new_user = create_entry(User, **user_data)

        if new_user:
            flash('New user created successfully!', 'success')
        else:
            flash('Error creating new user.', 'error')

        return redirect(url_for('admin.admin_dashboard'))
    if request.method=='GET':
        # Query all departments and roles
        departments = Department.query.all()
        roles = Role.query.all()
        return render_template('admin/new_user.html', departments=departments, roles=roles)

@admin_bp.route('/new_event', methods=['GET'])
def new_event():
    # Query the database for departments, users for Event Manager/Finance Manager, and event types
    departments = Department.query.all()
    event_managers = User.query.all()  # Assuming all users can be event managers
    finance_managers = User.query.all()  # Assuming all users can be finance managers
    event_types = EventType.query.all()
    
    return render_template('admin/new_event_creation.html', 
                           departments=departments, 
                           event_managers=event_managers, 
                           finance_managers=finance_managers,
                           event_types=event_types)

@admin_bp.route('/create_single_event', methods=['POST'])
def create_single_event():
    event_name = request.form.get('eventName')
    event_type = request.form.get('eventType')
    event_date = request.form.get('eventDate')
    department_id = request.form.get('department')
    event_manager_id = request.form.get('EveMan')  # Updated to match form name
    finance_manager_id = request.form.get('FinMan')  # Updated to match form name

    # Validate required fields
    if not event_name or not event_type or not event_date or not event_manager_id or not finance_manager_id:
        flash("Please fill in all required fields.")
        return redirect(url_for('admin.new_event'))

    try:
        event_date = datetime.strptime(event_date, "%Y-%m-%d")  # Convert to datetime object
    except ValueError:
        flash("Invalid date format. Please use YYYY-MM-DD.")
        return redirect(url_for('admin.new_event'))

    # Create and save the event
    new_event = Event(
        Name=event_name,
        Event_Type_ID=event_type,
        Date=event_date,
        Days=1,  # Default duration of 1 day for single event
        Dept_ID=department_id,
        Event_Manager=event_manager_id,
        Finance_Manager=finance_manager_id
    )
    db.session.add(new_event)
    db.session.commit()

    flash("Single Event Created Successfully!")
    return redirect(url_for('admin.new_event'))

@admin_bp.route('/create_multiple_events', methods=['POST'])
def create_multiple_events():
    from datetime import datetime

    # Main Event Details
    event_name = request.form.get('eventName')
    event_type = request.form.get('eventType')
    event_start_date = request.form.get('eventDate')
    department_id = request.form.get('department')
    event_manager_id = request.form.get('EveMan')
    finance_manager_id = request.form.get('FinMan')
    sub_event_count = request.form.get('subEventCount')

    # Validate main event data
    if not all([event_name, event_type, event_start_date, sub_event_count]):
        flash("Please fill in all required fields.")
        return redirect(url_for('admin.new_event'))

    try:
        event_start_date = datetime.strptime(event_start_date, "%Y-%m-%d")
    except ValueError:
        flash("Invalid start date format. Please use YYYY-MM-DD.")
        return redirect(url_for('admin.new_event'))

    # Collect unique sub-event dates
    unique_dates = set()
    for i in range(int(sub_event_count)):
        sub_event_date = request.form.get(f'subEventDate{i}')
        try:
            sub_event_date = datetime.strptime(sub_event_date, "%Y-%m-%d").date()
            unique_dates.add(sub_event_date)
        except ValueError:
            flash(f"Invalid date format for Sub-event {i+1}. Please use YYYY-MM-DD.")
            return redirect(url_for('admin.new_event'))

    # Set the 'Days' for the main event as the number of unique sub-event dates
    event_duration = len(unique_dates)

    # Check if the sub-event dates cover the specified number of unique days
    if len(unique_dates) != event_duration:
        flash(f"The sub-event dates must cover exactly {event_duration} unique days.")
        return redirect(url_for('admin.new_event'))

    # Create the main event
    new_event = Event(
        Name=event_name,
        Event_Type_ID=event_type,
        Date=event_start_date,
        Days=event_duration,  # Set the 'Days' as the number of unique dates
        Dept_ID=department_id,
        Event_Manager=event_manager_id,
        Finance_Manager=finance_manager_id
    )
    db.session.add(new_event)
    db.session.commit()

    # Create sub-events
    for i in range(int(sub_event_count)):
        sub_event_name = request.form.get(f'subEventName{i}')
        sub_event_type = request.form.get(f'subEventType{i}')
        sub_event_date = request.form.get(f'subEventDate{i}')
        sub_event_time = request.form.get(f'subEventTime{i}')
        sub_event_manager_id = request.form.get(f'subEventManager{i}')

        if not all([sub_event_name, sub_event_type, sub_event_date, sub_event_time]):
            flash(f"Sub-event {i+1} is missing required information.")
            continue

        sub_event_date = datetime.strptime(sub_event_date, "%Y-%m-%d").date()
        
        # Create the sub-event
        sub_event = SubEvent(
            Name=sub_event_name,
            Event_Type_ID=sub_event_type,
            Date=sub_event_date,
            Time=sub_event_time,
            Dept_ID=department_id,
            Event_ID=new_event.Event_ID,
            Sub_Event_Manager=sub_event_manager_id
        )
        db.session.add(sub_event)

    db.session.commit()
    flash("Multiple Events and Sub-Events Created Successfully!")
    return redirect(url_for('admin.new_event'))
    
@admin_bp.route('/view_events')
def view_events():
    return render_template('admin/view_events.html', events=get_event_data())

def get_event_data():
    """
    This function returns a list of dictionaries containing event data.
    The dictionary will be named event_card_data and it will have the following keys:
        "id", "event_name", "status", "type", "department", "event_manager"
    The status will be either "Upcoming", "Ongoing", or "Completed" based on the event's date.
    """
    
    # Initialize the data list
    event_card_data = []

    # Get the current date
    current_date = date.today()

    # Fetch all the events, sub-events, users, and departments from the database
    events = Event.query.all()
    sub_events = SubEvent.query.all()
    users = User.query.all()
    depts = Department.query.all()
    event_types = EventType.query.all()

    # Loop through the events and build the data for each
    for event in events:
        # Determine the event status based on the event date
        if event.Date > current_date:
            status = "Upcoming"
        elif event.Date == current_date:
            status = "Ongoing"
        else:
            status = "Completed"

        # Get the event type name using EventType model
        event_type = next((et.Event_Type_Name for et in event_types if et.Event_Type_ID == event.Event_Type_ID), "Unknown")

        # Get the department name using the Department model
        department = next((dept.Name for dept in depts if dept.Dept_ID == event.Dept_ID), "Unknown")

        # Get the event manager using the User model
        event_manager = next((user.Username for user in users if user.User_ID == event.Event_Manager), "Unknown")

        # Build the event card data
        event_card_data.append({
            "id": event.Event_ID,
            "event_name": event.Name,
            "status": status,
            "type": event_type,
            "department": department,
            "event_manager": event_manager
        })
    
    return event_card_data
    
def get_user_info(user):
    """Fetch and structure data for a single user, including related roles, departments."""
    
    # Fetch related role and department for the specified user
    roles = filter_data(Role, columns=["Role_ID", "Role_Name"])
    departments = filter_data(Department, columns=["Dept_ID", "Name"])

    # Convert role and department data into dictionaries for fast lookup
    roles_dict = {role.Role_ID: role.Role_Name for role in roles}
    departments_dict = {dept.Dept_ID: dept.Name for dept in departments}

    # Determine the user's role
    user_role = roles_dict.get(user.Role, "No Role Assigned")

    # Construct user info dictionary without events and sub-events
    user_info = {
        "id": user.User_ID,
        "name": user.Username or "User Name",
        "email": user.Email,
        "role": user_role,
        "department": departments_dict.get(user.Dept_ID, "No Department Assigned"),
        "verified": user.Verified  # Ensure Verified data is passed
    }
    print(user_info)
    return user_info

def get_user_table_data():
    # Fetch filtered data
    users = filter_data(User, None, ['User_ID', 'Username', 'Email', 'Role', 'Dept_ID'])
    depts = filter_data(Department, None, ['Dept_ID', 'Name'])
    roles = filter_data(Role, None, ['Role_ID', 'Role_Name'])
    
    # Create a mapping for quick lookup
    dept_dict = {dept.Dept_ID: dept.Name for dept in depts}
    role_dict = {role.Role_ID: role.Role_Name for role in roles}

    user_table_data = []
    for user in users:
        # Lookup department and role names
        department_name = dept_dict.get(user.Dept_ID, "N/A")
        role_name = role_dict.get(user.Role, "N/A")

        # Add user data to table
        row = {
            'user_id': user.User_ID,
            'Full Name': user.Username.title(),
            'Email': user.Email,
            'Role': role_name,
            'Department': department_name
        }
        user_table_data.append(row)

    # Print data for verification
    print(user_table_data)
    return user_table_data

@admin_bp.route('/view_user/<int:user_id>', methods=['GET'])
def view_user(user_id):
    """Route to view detailed information for a single user."""
    user = User.query.get(user_id)
    if not user:
        flash(f"User with ID {user_id} not found.", "error")
        return redirect(url_for('admin.admin_dashboard'))
    
    user_info = get_user_info(user)  # Retrieve structured user data
    return render_template('admin/view_user.html', user=user_info)

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """Route to edit an existing user."""
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('admin.admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', user.Username)
        email = request.form.get('email', user.Email)
        role_id = request.form.get('role')
        dept_id = request.form.get('department')

        if not username or not email:
            return redirect(url_for('admin.edit_user', user_id=user_id))

        user.Username = username
        user.Email = email
        if role_id:
            user.Role = role_id
        if dept_id:
            user.Dept_ID = dept_id

        db.session.commit()
        return redirect(url_for('admin.admin_dashboard'))

    roles = Role.query.all()
    departments = Department.query.all()
    return render_template('admin/edit_user.html', user=user, roles=roles, departments=departments)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST', 'GET'])
def delete_user(user_id):
    """Route to delete a user."""
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('admin.admin_dashboard'))

    filters = {'User_ID': user_id}
    if delete_entry(User, filters):
        return redirect(url_for('admin.admin_dashboard'))
    else:
        return redirect(url_for('admin.admin_dashboard'))

