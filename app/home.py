from flask import render_template, Blueprint, request, redirect, url_for, session, flash
from app.modules import validations
from .modules.models import Department, Role, User
from .modules.db_queries import filter_data, create_entry, update_entry
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

home_bp = Blueprint('home', __name__, url_prefix='')

@home_bp.route("/")
@home_bp.route("/index")
@home_bp.route("/home")
def index():
    return render_template("home/index.html")

@home_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        errors = {}

        # Validate email and password
        if not validations.is_valid_email(email):
            errors["email"] = "Invalid email address."
        if not validations.is_valid_password(password):
            errors["password"] = (
                "Password must be at least 8 characters, include uppercase, "
                "lowercase, a number, and a special character."
            )
        
        # If errors, render login form with error messages and input values
        if errors:
            return render_template("home/login.html", errors=errors, email=email, password=password)

        # Now check if the email and password are correct, and fetch user
        user = filter_data(User, filters={"Email": email})
        
        if not user or not check_password_hash(user[0].Password, password):  # If user doesn't exist or passwords don't match
            errors["general"] = "Invalid credentials. Please check your email and password."
            return render_template("home/login.html", errors=errors, email=email, password=password)

        # Check if the user is verified
        current_user = user[0]
        if current_user.Verified == 0:  # User is not verified
            errors["general"] = "Not a verified user, contact Admin."
            return render_template("home/login.html", errors=errors, email=email, password=password)

        # Check the role of the user
        role = current_user.role.Role_Name  # Assuming the role is an object and has a 'Role_Name' attribute

        # Create session for authenticated user
        session['user_id'] = current_user.User_ID
        session['username'] = current_user.Username
        session['email'] = current_user.Email
        session['role'] = role
        session.permanent = True  # Make session persistent

        # Redirect based on role
        if role == 'Admin':
            return redirect(url_for('admin.admin_dashboard'))
        elif role == 'Event Manager':
            return redirect(url_for('event_manager.event_manager', user_id=current_user.User_ID))
        elif role == 'Finance Manager':
            return redirect(url_for('finance_manager.finance_manager', user_id=current_user.User_ID))

        # If role is not found or any other case, redirect to a default page (home, for example)
        return redirect(url_for("home.index"))
    
    # Render the login page for GET requests
    return render_template("home/login.html")

@home_bp.route("/logout")
def logout():
    """Log out the current user by clearing the session."""
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home.login'))

@home_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    error_message = None  # Initialize the error message variable
    
    if request.method == "POST":
        email = request.form.get("email")
        
        # Validate the email format
        if not validations.is_valid_email(email):
            error_message = "Invalid email format. Please enter a valid email address."
            return render_template("home/forgotpassword.html", error_message=error_message)
        
        # Check if the email exists in the User table
        try:
            user = User.query.filter_by(Email=email).first()
            if user:
                # Email exists, redirect to reset password page with user_id
                return redirect(url_for('home.reset_password', user_id=user.User_ID))
            else:
                # Email does not exist, show an error message
                error_message = "Incorrect email address. Please try again."
                return render_template("home/forgotpassword.html", error_message=error_message)
        except SQLAlchemyError as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template("home/forgotpassword.html", error_message=error_message)

    # GET request: simply render the forgot password page
    return render_template("home/forgotpassword.html", error_message=error_message)


@home_bp.route("/reset-password/<int:user_id>", methods=["GET", "POST"])
def reset_password(user_id):
    # If the method is POST, update the password
    if request.method == "POST":
        # Get the form values
        new_password = request.form.get("new-password")
        confirm_password = request.form.get("confirm-password")
        
        # Initialize error messages
        new_password_error = None
        confirm_password_error = None

        # Validate passwords
        if new_password != confirm_password:
            confirm_password_error = "Passwords do not match."
        
        if not validations.is_valid_password(new_password):  # Validate using the function in validations.py
            new_password_error = "Password must be at least 8 characters long, and include an uppercase letter, a number, and a special character."

        # If there are any errors, return the form with error messages
        if new_password_error or confirm_password_error:
            return render_template(
                "home/resetpassword.html",
                user_id=user_id,  # Pass user_id to the template
                new_password_error=new_password_error,
                confirm_password_error=confirm_password_error
            )

        # If no validation errors, update the password
        try:
            # Use the filter_data function to fetch the user
            user = filter_data(User, filters={'User_ID': user_id})
            
            if user:
                # Hash the new password before saving
                hashed_password = generate_password_hash(new_password)
                
                # Use the db_queries update function to save the new password
                updated_user = update_entry(User, {'User_ID': user_id}, {'Password': hashed_password})

                if updated_user:
                    return redirect(url_for('home.login'))  # Redirect to the login page after successful password reset
                else:
                    return render_template("home/resetpassword.html", error_message="Error updating password.", user_id=user_id)
            else:
                return render_template("home/resetpassword.html", error_message="User not found.", user_id=user_id)
        except SQLAlchemyError as e:
            return render_template("home/resetpassword.html", error_message=f"An error occurred: {str(e)}", user_id=user_id)

    # If GET request, just render the reset password form
    return render_template("home/resetpassword.html", user_id=user_id)


@home_bp.route("/signup", methods=["GET", "POST"])
def signup():
    # Fetch department and role data before processing POST or GET request
    departments = filter_data(Department, columns=["Dept_ID", "Name"])
    roles = filter_data(Role, columns=["Role_ID", "Role_Name"])

    # Initialize empty error messages dictionary
    error_messages = {
        "username": "",
        "email": "",
        "department": "",
        "password": "",
        "confirmPassword": "",
        "role": "",
    }

    if request.method == "POST":
        # Get form data
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmPassword")
        department_id = request.form.get("department")
        role_id = request.form.get("role")

        # Validate each field
        if not validations.is_valid_username(username):
            error_messages["username"] = "Username must be 3-30 characters long and alphanumeric."
        if not validations.is_valid_email(email):
            error_messages["email"] = "Please enter a valid email address."
        if not validations.is_valid_department(department_id):
            error_messages["department"] = "Please select a department."
        if not validations.is_valid_password(password):
            error_messages["password"] = "Password must be at least 8 characters long with uppercase, lowercase, number, and special character."
        if password != confirm_password:
            error_messages["confirmPassword"] = "Passwords do not match."
        if not validations.is_valid_role(role_id):
            error_messages["role"] = "Please select a role."

        # Check if there are any errors
        if any(error_messages.values()):
            return render_template("home/signup.html", error_messages=error_messages, departments=departments, roles=roles)

        # If no errors, proceed with creating the user
        existing_user = filter_data(User, filters={"Username": username}) or filter_data(User, filters={"Email": email})
        if existing_user:
            error_messages["email"] = "Username or Email already exists. Please use a different one."
            return render_template("home/signup.html", error_messages=error_messages, departments=departments, roles=roles)

        # Create new user entry with hashed password
        hashed_password = generate_password_hash(password)
        new_user = {
            "Username": username,
            "Email": email,
            "Password": hashed_password,
            "Role": role_id,
            "Dept_ID": department_id,
            "Verified": 0  # Default unverified status
        }

        try:
            create_entry(User, **new_user)
            return redirect(url_for('home.login'))  # Redirect to login page after successful signup
        except SQLAlchemyError:
            error_messages["general"] = "An error occurred while creating your account. Please try again."
            return render_template("home/signup.html", error_messages=error_messages, departments=departments, roles=roles)

    # For GET request, departments and roles are already defined above
    return render_template("home/signup.html", error_messages=error_messages, departments=departments, roles=roles)

    