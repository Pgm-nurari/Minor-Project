from flask import render_template,Blueprint

home_bp = Blueprint('home', __name__, url_prefix='/main')

@home_bp.route("/home")
def index():
    return render_template("home/index.html")

@home_bp.route("/login")
def login():
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
