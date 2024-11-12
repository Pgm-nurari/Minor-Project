from flask import Blueprint, render_template, redirect, request, flash, url_for
from . import db
from .modules.models import Department, Role, User, EventType, Event, SubEvent
from .modules.db_queries import create_entry
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from .test_data import test_user_data, test_event_data


admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_dashboard():
    users = User.query.all()
    print(users)
    return render_template('admin/admin_dash.html',events=test_event_data, users=test_user_data)

@admin_bp.route('/event_details/<int:event_id>')
def event_details(event_id):
    # Get the event based on the ID
    event = next((event for event in test_event_data if int(event['id']) == event_id), None)
    if event is None:
        return "Event not found", 404  # Add a 404 error page or message
    return render_template('admin/event_details.html', event=event)


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
    return render_template('admin/view_events.html', events=test_event_data)