import os
from flask import Flask, render_template
from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig
from pocketbase import PocketBase
from pocketbase.client import FileUpload

app = Flask(__name__)

# Flask will pick up FLASK_ENV from .flaskenv, so no need to manually check
app.config.from_object({
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}[app.config.get('ENV', 'development')])

# Initialize PocketBase client
client = PocketBase('https://finsight.pockethost.io/')  

@app.route('/')
def home_page():
    navigations = [
        ('Home', 'dashboard'),  # Redirects to dashboard
        ('About Us', 'section'), 
        ('Contact Us', 'section'),
        ('Login', 'button'),
        ('Sign Up', 'button')
    ]
    return render_template('index.html', navbar=navigations)

@app.route('/admin')
def admin_page():
    navigations = [
        ('admin', 'dashboard'),  # Redirects to admin dashboard
        ('Users', 'section'),
        ('Events', 'section'),
        ('Notifications', 'button'),
        ('Logout', 'button')
    ]
    return render_template('adminpage.html', navbar=navigations)

@app.route('/event-manager')
def event_manager_page():
    navigations = [
        ('event manager', 'dashboard'),  # Redirects to event manager dashboard
        ('Transactions', 'section'),
        ('Events', 'section'),
        ('Notifications', 'button'),
        ('Logout', 'button')
    ]
    return render_template('eventmanagerpage.html', navbar=navigations)

@app.route('/finance-manager')
def finance_manager_page():
    navigations = [
        ('finance manager', 'dashboard'),  # Redirects to finance manager dashboard
        ('Events', 'section'),
        ('Transactions', 'section'),
        ('Analysis', 'section'),
        ('Charts', 'section'),
        ('Notifications', 'button'),
        ('Logout', 'button')
    ]
    return render_template('financemanagerpage.html', navbar=navigations)

if __name__ == '__main__':
    app.run(debug=True)
