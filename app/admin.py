from flask import Blueprint, render_template, redirect, request, flash, url_for, get_flashed_messages, session, jsonify  
from . import db
from .modules.models import *
from .modules.db_queries import *
from .modules.activity_logger import log_activity, create_notification
from .auth import role_required, get_current_user
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import asc, desc
from sqlalchemy import func
from datetime import datetime, date

from werkzeug.security import generate_password_hash, check_password_hash

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def check_admin_access():
    """Check if user is logged in and has Admin role before accessing any admin route."""
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('home.login'))
    
    if session.get('role') != 'Admin':
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('home.index'))

@admin_bp.route('/')
def admin_dashboard():
    # Retrieve all users
    users = filter_data(User)
    user_data = [get_user_info(user) for user in users]

    # Render the template with the structured user data
    return render_template('admin/admin_dash.html', data=user_data, users_table = get_user_table_data(), events=get_event_data())

@admin_bp.route('/event_details/<int:event_id>', methods=['GET', 'POST'])
def event_details(event_id):
    # Fetch the event from the database
    event = Event.query.get(event_id)
    
    if event is None:
        return "Event not found", 404  # Return 404 if event doesn't exist

    # Get the event manager and finance manager
    event_manager = event.event_manager if event.event_manager else None
    finance_manager = event.finance_manager if event.finance_manager else None

    # Fetch the related sub-events
    sub_events = SubEvent.query.filter_by(Event_ID=event_id).all()
    
    # Fetch the budget for the event
    budget = Budget.query.filter_by(Event_ID=event_id).first()

    if request.method == 'POST':
        # Handle form submission for budget allocation or update
        budget_amount = request.form.get('amount')
        budget_notes = request.form.get('notes')

        if budget:  # Update budget
            updated_budget = update_entry(Budget, 
                                          filters={'Event_ID': event_id}, 
                                          updates={'Amount': budget_amount, 'Notes': budget_notes})
        else:  # Create new budget entry
            updated_budget = create_entry(Budget, 
                                          Amount=budget_amount, 
                                          Notes=budget_notes, 
                                          Event_ID=event_id)

        # Redirect to the same page after creating or updating the budget
        return redirect(url_for('admin.event_details', event_id=event_id))
    
    # Pass all the data to the template
    return render_template('admin/event_details.html', 
                           event=event,
                           event_manager=event_manager,
                           finance_manager=finance_manager,
                           sub_events=sub_events,
                           budget=budget)

@admin_bp.route('/view_events')
def view_events():
    return render_template('admin/view_events.html', events=get_event_data())
@admin_bp.route('/new_event', methods=['GET'])
def new_event():
    # Query database for required data
    departments = Department.query.all()
    event_types = EventType.query.all()
    event_managers = User.query.join(Role).filter(Role.Role_Name == 'Event Manager').all()
    finance_managers = User.query.join(Role).filter(Role.Role_Name == 'Finance Manager').all()
    
    print(event_managers)

    return render_template(
        'admin/new_event_creation.html',
        departments=departments,
        event_managers=event_managers,
        finance_managers=finance_managers,
        event_types=event_types
    )


@admin_bp.route('/create_single_event', methods=['POST'])
def create_single_event():
    try:
        event_name = request.form.get('eventName')
        event_type = request.form.get('eventType')
        event_date = request.form.get('eventDate')
        department_id = request.form.get('department')
        event_manager_id = request.form.get('EveMan')
        finance_manager_id = request.form.get('FinMan')

        # Validate required fields
        if not all([event_name, event_type, event_date, department_id, event_manager_id, finance_manager_id]):
            return jsonify({"status": "error", "message": "All fields are required!"}), 400

        # Parse date
        event_date = datetime.strptime(event_date, "%Y-%m-%d")

        # Create and save the event
        new_event = Event(
            Name=event_name,
            Event_Type_ID=event_type,
            Date=event_date,
            Days=1,  # Default duration for single events
            Dept_ID=department_id,
            Event_Manager=event_manager_id,
            Finance_Manager=finance_manager_id
        )
        db.session.add(new_event)
        db.session.commit()
        
        # Notify Event Manager
        create_notification(
            user_id=event_manager_id,
            title='New Event Assigned',
            message=f'You have been assigned as Event Manager for "{event_name}" scheduled on {event_date.strftime("%B %d, %Y")}',
            notification_type='success',
            event_id=new_event.Event_ID
        )
        
        # Notify Finance Manager
        create_notification(
            user_id=finance_manager_id,
            title='New Event Assigned',
            message=f'You have been assigned as Finance Manager for "{event_name}" scheduled on {event_date.strftime("%B %d, %Y")}',
            notification_type='success',
            event_id=new_event.Event_ID
        )
        
        # Log activity
        log_activity(
            user_id=1,  # Admin user
            action='created',
            entity_type='Event',
            entity_id=new_event.Event_ID,
            description=f'Admin created event "{event_name}"'
        )
        
        return jsonify({"status": "success", "message": "Single event created successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Error creating single event: {e}"}), 500

@admin_bp.route('/create_multiple_events', methods=['POST'])
def create_multiple_events():
    try:
        event_name = request.form.get('eventName')
        event_type = request.form.get('eventType')
        event_start_date = request.form.get('eventDate')
        department_id = request.form.get('department')
        event_manager_id = request.form.get('EveMan')
        finance_manager_id = request.form.get('FinMan')
        sub_event_count = int(request.form.get('subEventCount', 0))

        # Validate main event fields
        if not all([event_name, event_type, event_start_date]) or sub_event_count < 1:
            return jsonify({"status": "error", "message": "All fields are required!"}), 400

        # Parse main event start date
        event_start_date = datetime.strptime(event_start_date, "%Y-%m-%d")

        # Collect sub-event dates
        unique_dates = set()
        sub_events = []
        for i in range(sub_event_count):
            sub_event_name = request.form.get(f'subEventName{i}')
            sub_event_type = request.form.get(f'subEventType{i}')
            sub_event_date = request.form.get(f'subEventDate{i}')
            sub_event_time = request.form.get(f'subEventTime{i}')
            sub_event_manager_id = request.form.get(f'subEventManager{i}')

            if not all([sub_event_name, sub_event_type, sub_event_date, sub_event_time, sub_event_manager_id]):
                return jsonify({"status": "error", "message": f"Sub-event {i+1} is missing required fields!"}), 400

            # Parse sub-event date
            sub_event_date = datetime.strptime(sub_event_date, "%Y-%m-%d").date()
            unique_dates.add(sub_event_date)

            sub_events.append(SubEvent(
                Name=sub_event_name,
                Event_Type_ID=sub_event_type,
                Date=sub_event_date,
                Time=sub_event_time,
                Dept_ID=department_id,
                Sub_Event_Manager=sub_event_manager_id
            ))

        # Main event duration
        event_duration = len(unique_dates)

        # Create main event
        new_event = Event(
            Name=event_name,
            Event_Type_ID=event_type,
            Date=event_start_date,
            Days=event_duration,
            Dept_ID=department_id,
            Event_Manager=event_manager_id,
            Finance_Manager=finance_manager_id
        )
        db.session.add(new_event)
        db.session.commit()

        # Associate sub-events with the main event
        for sub_event in sub_events:
            sub_event.Event_ID = new_event.Event_ID
            db.session.add(sub_event)
        db.session.commit()
        
        # Notify main Event Manager
        create_notification(
            user_id=event_manager_id,
            title='New Multi-Day Event Assigned',
            message=f'You have been assigned as Event Manager for "{event_name}" ({event_duration} days) with {len(sub_events)} sub-events',
            notification_type='success',
            event_id=new_event.Event_ID
        )
        
        # Notify main Finance Manager
        create_notification(
            user_id=finance_manager_id,
            title='New Multi-Day Event Assigned',
            message=f'You have been assigned as Finance Manager for "{event_name}" ({event_duration} days) with {len(sub_events)} sub-events',
            notification_type='success',
            event_id=new_event.Event_ID
        )
        
        # Notify each sub-event manager
        for sub_event in sub_events:
            create_notification(
                user_id=sub_event.Sub_Event_Manager,
                title='Sub-Event Assignment',
                message=f'You have been assigned to manage sub-event "{sub_event.Name}" under "{event_name}"',
                notification_type='info',
                event_id=new_event.Event_ID
            )
        
        # Log activity
        log_activity(
            user_id=1,  # Admin user
            action='created',
            entity_type='Event',
            entity_id=new_event.Event_ID,
            description=f'Admin created multi-day event "{event_name}" with {len(sub_events)} sub-events'
        )

        return jsonify({"status": "success", "message": "Multiple events and sub-events created successfully!"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": f"Error creating multiple events: {e}"}), 500


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

        # Create a new user with a default hashed password
        default_password = generate_password_hash('ChangeMe@123')  # Default password that user must change
        user_data = {
            'Username': username,
            'Email': email,
            'Role': role.Role_ID,  
            'Dept_ID': department.Dept_ID,  
            'Password': default_password
        }

        # Add the new user to the database using the create_entry function
        new_user = create_entry(User, **user_data)

        if new_user:
            # Send welcome notification to new user
            from app.modules.activity_logger import create_notification, log_activity
            create_notification(
                user_id=new_user.User_ID,
                title='Welcome to FinSight!',
                message=f'Your account has been created. Username: {username}. Default password: ChangeMe@123. Please change your password after first login.',
                notification_type='info'
            )
            
            # Log activity
            log_activity(
                user_id=session.get('user_id', 1),
                action='created',
                entity_type='User',
                entity_id=new_user.User_ID,
                description=f'Created new user: {username} ({role.Role_Name})'
            )
            
            flash('New user created successfully!', 'success')
        else:
            flash('Error creating new user.', 'error')

        return redirect(url_for('admin.admin_dashboard'))
    if request.method=='GET':
        # Query all departments and roles
        departments = Department.query.all()
        roles = Role.query.all()
        return render_template('admin/new_user.html', departments=departments, roles=roles)

@admin_bp.route('/view_user/<int:user_id>', methods=['GET'])
def view_user(user_id):
    """Route to view detailed information for a single user."""
    user = User.query.get(user_id)
    if not user:
        flash(f"User with ID {user_id} not found.", "error")
        return redirect(url_for('admin.admin_dashboard'))
    
    return render_template('admin/view_user.html', user=user)

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    """Route to edit an existing user."""
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('admin.users_table'))

    if request.method == 'POST':
        username = request.form.get('username', user.Username)
        email = request.form.get('email', user.Email)
        role_id = request.form.get('role')
        dept_id = request.form.get('department')

        if not username or not email:
            flash('Username and email are required.', 'error')
            return redirect(url_for('admin.edit_user', user_id=user_id))

        # Check if role is being changed
        role_changed = False
        old_role = None
        if role_id and int(role_id) != user.Role:
            role_changed = True
            old_role_obj = Role.query.get(user.Role)
            new_role_obj = Role.query.get(role_id)
            old_role = old_role_obj.Role_Name if old_role_obj else "Unknown"
            new_role = new_role_obj.Role_Name if new_role_obj else "Unknown"
            user.Role = role_id
            user.Verified = 0  # Require re-authorization when role changes
        
        user.Username = username
        user.Email = email
        user.modified_date = datetime.now()
        
        if dept_id:
            user.Dept_ID = dept_id

        db.session.commit()
        
        # Notify user if role changed
        if role_changed:
            from app.modules.activity_logger import create_notification, log_activity
            create_notification(
                user_id=user.User_ID,
                title='Role Updated',
                message=f'Your role has been changed from {old_role} to {new_role}. Please contact admin for re-authorization.',
                notification_type='warning'
            )
            
            # Log activity
            log_activity(
                user_id=session.get('user_id', 1),
                action='updated',
                entity_type='User',
                entity_id=user.User_ID,
                description=f'Changed role of {username} from {old_role} to {new_role}'
            )
            
            flash('User updated successfully! Role change requires admin authorization.', 'warning')
        else:
            from app.modules.activity_logger import log_activity
            log_activity(
                user_id=session.get('user_id', 1),
                action='updated',
                entity_type='User',
                entity_id=user.User_ID,
                description=f'Updated user {username}'
            )
            flash('User updated successfully!', 'success')
            
        return redirect(url_for('admin.view_user', user_id=user_id))

    roles = Role.query.all()
    departments = Department.query.all()
    return render_template('admin/new_user.html', user=user, roles=roles, departments=departments)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST', 'GET'])
def delete_user(user_id):
    """Route to delete a user."""
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('admin.admin_dashboard'))

    # Check if the user is associated with any event or sub-event
    associated_event = Event.query.filter(
        (Event.event_manager == user) | (Event.finance_manager == user)
    ).first()

    associated_sub_event = SubEvent.query.filter(
        SubEvent.sub_event_manager == user
    ).first()

    if associated_event or associated_sub_event:
        # If the user is associated with an event or sub-event, prevent deletion
        flash("This user cannot be deleted as they are linked to an event or sub-event.", "warning")
        return redirect(url_for('admin.admin_dashboard'))

    # If no association, proceed with deletion
    filters = {'User_ID': user_id}
    if delete_entry(User, filters):
        flash("User deleted successfully.", "success")
        return redirect(url_for('admin.admin_dashboard'))
    else:
        flash("There was an issue deleting the user. Please try again.", "danger")
        return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/users')
def users_table():
    # Get parameters for sorting and filtering from the request
    sort_key = request.args.get('sort_key', 'username')  # Default sorting by 'username'
    sort_order = request.args.get('sort_order', 'asc')  # Default sorting order is ascending

    # Filter parameters (role, department, username)
    filter_role = request.args.get('filter_role', '')
    filter_department = request.args.get('filter_department', '')
    filter_username = request.args.get('filter_username', '')

    # Get the filtered and sorted user data from the database
    user_table_data = get_user_table_data(
        sort_key=sort_key,
        sort_order=sort_order,
        filter_role=filter_role,
        filter_department=filter_department,
        filter_username=filter_username
    )
    users = filter_data(User)
    user_data = [get_user_info(user) for user in users]

    # Pass the filters as part of the context so they can be included in the URLs for sorting
    return render_template('admin/user_table.html', 
                           users_table=user_table_data,
                           filter_role=filter_role,
                           filter_department=filter_department,
                           filter_username=filter_username,
                           sort_key=sort_key,
                           sort_order=sort_order,data=user_data)

@admin_bp.route('/authorize/<int:user_id>', methods=['POST'])
def authorize_user(user_id):
    """Route to handle user authorization by updating Verified status."""
    try:
        # Find the user by ID
        user = User.query.get(user_id)
        if not user:
            flash("User not found.", "error")
            return redirect(url_for('admin.users_table'))
        
        # Check if the user is already authorized
        if user.Verified == 1:
            flash("User is already authorized.", "info")
            return redirect(url_for('admin.users_table'))
        
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

def get_user_table_data(sort_key='username', sort_order='asc', filter_role='', filter_department='', filter_username=''):
    query = db.session.query(User.User_ID, User.Username, User.Email, User.Role, User.Dept_ID)
    
    # Apply filters if specified
    if filter_role:
        query = query.filter(User.Role == filter_role)
    if filter_department:
        query = query.filter(User.Dept_ID == filter_department)
    if filter_username:
        query = query.filter(User.Username.ilike(f'%{filter_username}%'))

    # Apply sorting (consider descending order if specified)
    if sort_order == 'desc':
        sort_func = desc
    else:
        sort_func = asc

    # Dynamically apply sorting based on the sort_key
    if sort_key == 'username':
        query = query.order_by(sort_func(User.Username))
    elif sort_key == 'email':
        query = query.order_by(sort_func(User.Email))
    elif sort_key == 'role':
        query = query.order_by(sort_func(User.Role))
    elif sort_key == 'department':
        query = query.order_by(sort_func(User.Dept_ID))

    # Execute query and fetch the results
    users = query.all()

    # Fetch departments and roles for lookup
    depts = filter_data(Department, None, ['Dept_ID', 'Name'])
    roles = filter_data(Role, None, ['Role_ID', 'Role_Name'])

    # Create dictionaries for quick lookup
    dept_dict = {dept.Dept_ID: dept.Name for dept in depts}
    role_dict = {role.Role_ID: role.Role_Name for role in roles}

    user_table_data = []
    for user in users:
        # Lookup department and role names using the dictionaries
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

    return user_table_data

def get_event_data():
    """
    This function returns a dictionary containing events grouped by their status.
    The dictionary will have the following keys: "Upcoming", "Ongoing", and "Completed",
    each containing a list of event data (dictionaries).
    Each event dictionary will have the following keys:
        "id", "event_name", "status", "type", "department", "event_manager", "finance_manager"
    """

    # Initialize the dictionary to store events by status
    grouped_event_data = {'Upcoming': [], 'Ongoing': [], 'Completed': []}

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

        # Build the event card data dictionary
        event_data = {
            "id": event.Event_ID,
            "event_name": event.Name,
            "status": status,
            "type": event_type,
            "department": department,
            "event_manager": event_manager,
        }

        # Append the event data to the appropriate status list in the dictionary
        grouped_event_data[status].append(event_data)
    return grouped_event_data
    
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
    #User Info Display....
    # print(user_info)
    return user_info

@admin_bp.route('/view_sub_event/<int:sub_event_id>')
def view_sub_event(sub_event_id):
    sub_event = SubEvent.query.get(sub_event_id)
    if not sub_event:
        return "Sub-Event not found", 404
    return render_template('admin/view_sub_event.html', sub_event=sub_event)

@admin_bp.route('/create_sub_event/<int:event_id>', methods=['GET', 'POST'])
def create_sub_event(event_id):
    parent_event = Event.query.get(event_id)
    if not parent_event:
        flash("Event not found.", "error")
        return redirect(url_for('admin.view_events'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        time = request.form.get('time')
        
        if name and date and time:
            new_sub_event = SubEvent(
                Name=name,
                Date=datetime.strptime(date, '%Y-%m-%d').date(),
                Time=datetime.strptime(time, '%H:%M').time(),
                Event_ID=event_id
            )
            db.session.add(new_sub_event)
            db.session.commit()
            
            flash("Sub-event created successfully!", "success")
            return redirect(url_for('admin.event_details', event_id=event_id))
        else:
            flash("All fields are required.", "error")
    
    return render_template('admin/new_sub_event.html', parent_event=parent_event)

@admin_bp.route('/edit_sub_event/<int:sub_event_id>', methods=['GET', 'POST'])
def edit_sub_event(sub_event_id):
    sub_event = SubEvent.query.get(sub_event_id)
    if not sub_event:
        flash("Sub-Event not found.", "error")
        return redirect(url_for('admin.view_events'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        time = request.form.get('time')
        
        if name and date and time:
            sub_event.Name = name
            sub_event.Date = datetime.strptime(date, '%Y-%m-%d').date()
            sub_event.Time = datetime.strptime(time, '%H:%M').time()
            db.session.commit()
            
            flash("Sub-event updated successfully!", "success")
            return redirect(url_for('admin.event_details', event_id=sub_event.Event_ID))
        else:
            flash("All fields are required.", "error")
    
    return render_template('admin/new_sub_event.html', sub_event=sub_event)

@admin_bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get(event_id)
    if not event:
        flash("Event not found.", "error")
        return redirect(url_for('admin.view_events'))

    # Check for sub-events
    sub_events = SubEvent.query.filter_by(Event_ID=event_id).all()

    if request.method == 'POST':
        # Update fields
        event_type = request.form.get('eventType')
        event_manager = request.form.get('EveMan')
        finance_manager = request.form.get('FinMan')
        department = request.form.get('department')
        event_date = request.form.get('eventDate')

        # Track changes for notifications
        manager_changed = False
        old_event_manager = event.Event_Manager
        old_finance_manager = event.Finance_Manager
        
        if event_type:
            event.Event_Type_ID = event_type
        if event_manager and int(event_manager) != event.Event_Manager:
            manager_changed = True
            event.Event_Manager = event_manager
        if finance_manager and int(finance_manager) != event.Finance_Manager:
            manager_changed = True
            event.Finance_Manager = finance_manager
        if department:
            event.Dept_ID = department
        
        # Only update date if no sub-events exist
        if event_date and not sub_events:
            event.Date = datetime.strptime(event_date, '%Y-%m-%d').date()
        elif event_date and sub_events:
            flash("Event date cannot be changed when sub-events exist.", "warning")

        event.modified_date = datetime.now()
        db.session.commit()

        # Send notifications if managers changed
        if manager_changed:
            from app.modules.activity_logger import create_notification, log_activity
            
            # Notify old managers they were removed
            if old_event_manager and old_event_manager != event.Event_Manager:
                create_notification(
                    user_id=old_event_manager,
                    title='Event Manager Assignment Removed',
                    message=f'You have been removed as Event Manager from event "{event.Name}"',
                    notification_type='warning',
                    event_id=event_id
                )
            
            if old_finance_manager and old_finance_manager != event.Finance_Manager:
                create_notification(
                    user_id=old_finance_manager,
                    title='Finance Manager Assignment Removed',
                    message=f'You have been removed as Finance Manager from event "{event.Name}"',
                    notification_type='warning',
                    event_id=event_id
                )
            
            # Notify new managers they were added
            if event_manager and int(event_manager) != old_event_manager:
                create_notification(
                    user_id=int(event_manager),
                    title='New Event Assignment',
                    message=f'You have been assigned as Event Manager for event "{event.Name}"',
                    notification_type='success',
                    event_id=event_id
                )
            
            if finance_manager and int(finance_manager) != old_finance_manager:
                create_notification(
                    user_id=int(finance_manager),
                    title='New Event Assignment',
                    message=f'You have been assigned as Finance Manager for event "{event.Name}"',
                    notification_type='success',
                    event_id=event_id
                )
            
            # Log activity
            log_activity(
                user_id=session.get('user_id', 1),
                action='updated',
                entity_type='Event',
                entity_id=event_id,
                description=f'Updated managers for event "{event.Name}"'
            )

        flash("Event updated successfully!", "success")
        return redirect(url_for('admin.event_details', event_id=event_id))

    # Fetch all required data for dropdowns
    departments = Department.query.all()
    event_types = EventType.query.all()
    event_managers = User.query.join(Role).filter(Role.Role_Name == 'Event Manager').all()
    finance_managers = User.query.join(Role).filter(Role.Role_Name == 'Finance Manager').all()

    return render_template('admin/new_event_creation.html', 
                           event=event,
                           sub_events=sub_events,
                           departments=departments,
                           event_types=event_types,
                           event_managers=event_managers,
                           finance_managers=finance_managers)


@admin_bp.route('/profile')
def admin_profile():
    """Display admin profile page"""
    try:
        # For now, assuming admin user_id is 1 or can be retrieved from session
        # You should modify this to get the actual logged-in admin user ID
        admin_user_id = 1  # TODO: Get from session
        user = User.query.get_or_404(admin_user_id)
        
        return render_template('admin/profile.html', user=user)
    except Exception as e:
        flash(f"Error loading profile: {str(e)}", "danger")
        return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_admin_profile():
    """Edit admin profile"""
    try:
        admin_user_id = 1  # TODO: Get from session
        user = User.query.get_or_404(admin_user_id)
        
        if request.method == 'POST':
            # Get form data
            username = request.form.get('username')
            email = request.form.get('email')
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            # Update username and email
            old_username = user.Username
            old_email = user.Email
            
            user.Username = username
            user.Email = email
            
            # Handle password change if provided
            if current_password and new_password:
                # Verify current password
                if not check_password_hash(user.Password, current_password):
                    flash("Current password is incorrect", "danger")
                    return redirect(url_for('admin.edit_admin_profile'))
                
                # Check if passwords match
                if new_password != confirm_password:
                    flash("New passwords do not match", "danger")
                    return redirect(url_for('admin.edit_admin_profile'))
                
                # Update password
                user.Password = generate_password_hash(new_password)
                log_activity(
                    user_id=admin_user_id,
                    action='updated',
                    entity_type='User',
                    entity_id=admin_user_id,
                    description=f"Admin changed their password"
                )
            
            # Save changes
            db.session.commit()
            
            # Log the activity
            changes = []
            if old_username != username:
                changes.append(f"username from '{old_username}' to '{username}'")
            if old_email != email:
                changes.append(f"email from '{old_email}' to '{email}'")
            
            if changes:
                log_activity(
                    user_id=admin_user_id,
                    action='updated',
                    entity_type='User',
                    entity_id=admin_user_id,
                    description=f"Admin updated profile: {', '.join(changes)}"
                )
            
            flash("Profile updated successfully", "success")
            return redirect(url_for('admin.admin_profile'))
        
        return render_template('admin/edit_profile.html', user=user)
    
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating profile: {str(e)}", "danger")
        return redirect(url_for('admin.admin_profile'))


@admin_bp.route('/notifications')
def notifications():
    """Display notifications for admin"""
    try:
        admin_user_id = 1  # TODO: Get from session
        
        # Get all notifications for this user, ordered by most recent
        notifications_list = Notification.query.filter_by(User_ID=admin_user_id).order_by(Notification.Created_At.desc()).all()
        unread_count = Notification.query.filter_by(User_ID=admin_user_id, Is_Read=False).count()
        
        return render_template('admin/notifications.html', 
                             notifications=notifications_list,
                             unread_count=unread_count)
    except Exception as e:
        flash(f"Error loading notifications: {str(e)}", "danger")
        return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    """Mark a single notification as read"""
    try:
        from .modules.activity_logger import mark_notification_read
        mark_notification_read(notification_id)
        flash("Notification marked as read", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for('admin.notifications'))


@admin_bp.route('/notifications/mark-all-read', methods=['POST'])
def mark_all_notifications_read():
    """Mark all notifications as read"""
    try:
        admin_user_id = 1  # TODO: Get from session
        from .modules.activity_logger import mark_all_notifications_read
        mark_all_notifications_read(admin_user_id)
        flash("All notifications marked as read", "success")
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
    return redirect(url_for('admin.notifications'))


@admin_bp.route('/activity-log')
def activity_log():
    """Display activity log"""
    try:
        # Get all activity logs, ordered by most recent (limit to 100 for performance)
        activities = ActivityLog.query.order_by(ActivityLog.Timestamp.desc()).limit(100).all()
        
        return render_template('admin/activity_log.html', activities=activities)
    except Exception as e:
        flash(f"Error loading activity log: {str(e)}", "danger")
        return redirect(url_for('admin.admin_dashboard'))

