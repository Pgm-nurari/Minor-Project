# app/auth.py

from functools import wraps
from flask import session, redirect, url_for, flash
from .modules.models import User

def login_required(f):
    """Decorator to require login for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('home.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    """Decorator to require specific role(s) for a route."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in to access this page.', 'error')
                return redirect(url_for('home.login'))
            
            if 'role' not in session or session['role'] not in roles:
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('home.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Get the current logged-in user from session."""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None
