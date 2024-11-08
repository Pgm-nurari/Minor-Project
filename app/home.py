from flask import render_template, Blueprint, request, redirect, url_for, flash
from app.modules import validations

home_bp = Blueprint('home', __name__, url_prefix='/main')

@home_bp.route("/home")
def index():
    return render_template("home/index.html")

@home_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Validation
        errors = {}
        if not validations.is_valid_email(email):
            errors["email"] = "Invalid email address."
        if not validations.is_valid_password(password):
            errors["password"] = (
                "Password must be at least 8 characters, include uppercase, "
                "lowercase, a number, and a special character."
            )
        
        # If there are errors, re-render the login page with error messages
        if errors:
            return render_template("home/login.html", errors=errors)
        
        # If validation passes, proceed with login logic
        flash("Login successful!", "success")
        return redirect(url_for("home.index"))

    # If GET request, just render the login form
    return render_template("home/login.html")

@home_bp.route("/signup")
def signup():
    return render_template("home/signup.html")

@home_bp.route("/forgot-password")
def forgot_password():
    return render_template("home/forgotpassword.html")

@home_bp.route("/reset-password")
def reset_password():
    return render_template("home/resetpassword.html")
