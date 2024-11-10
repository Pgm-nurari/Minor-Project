from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, DecimalField, BooleanField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Email, Length, EqualTo, Regexp
from app.modules import validations

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
        if not validations.is_valid_email(email):
            errors["email"] = "Invalid email address."
        if not validations.is_valid_password(password):
            errors["password"] = (
                "Password must be at least 8 characters, include uppercase, "
                "lowercase, a number, and a special character."
            )
        if errors:
            return render_template("home/login.html", errors=errors, email=email, password=password)
        return redirect(url_for("home.index"))
    return render_template("home/login.html")

@home_bp.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("home/signup.html")

@home_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    return render_template("home/forgotpassword.html")

@home_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    return render_template("home/resetpassword.html")
