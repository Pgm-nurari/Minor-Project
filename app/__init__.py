# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config
import mysql.connector
from mysql.connector import Error
from urllib.parse import urlparse
import os

# Initialize SQLAlchemy without an app instance here
db = SQLAlchemy()

def create_database_if_not_exists(db_uri):
    """Create the database if it doesn't exist"""
    try:
        # Parse the database URI
        parsed = urlparse(db_uri)
        
        # Extract connection details
        username = parsed.username
        # URL decode the password (it's URL-encoded in the URI)
        from urllib.parse import unquote
        password = unquote(parsed.password) if parsed.password else ''
        host = parsed.hostname or 'localhost'
        database_name = parsed.path.lstrip('/')
        
        # Connect to MySQL server without specifying database
        connection = mysql.connector.connect(
            host=host,
            user=username,
            password=password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check if database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if database_name not in databases:
                # Create database
                cursor.execute(f"CREATE DATABASE {database_name}")
                print(f"✓ Database '{database_name}' created successfully")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"⚠ Database creation error: {e}")
        return False
    except Exception as e:
        print(f"⚠ Unexpected error: {e}")
        return False

def initialize_database(app):
    """Initialize database and create tables if they don't exist"""
    try:
        # Create database if it doesn't exist
        create_database_if_not_exists(app.config['SQLALCHEMY_DATABASE_URI'])
        
        # Import models to register them
        from .modules import models
        
        # Create tables if they don't exist
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if not existing_tables:
            print("⚠ No tables found. Creating database schema...")
            db.create_all()
            print("✓ Database tables created successfully")
            print("\n📝 Next step: Run 'python scripts/populate_db.py' to add sample data\n")
        else:
            print(f"✓ Database connected ({len(existing_tables)} tables found)")
            
        return True
    except Exception as e:
        print(f"✗ Database initialization error: {e}")
        return False

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize the db with the app
    db.init_app(app)

    # Register blueprints
    from . import routes
    routes.register_blueprints(app)

    # Initialize database and create tables if needed
    with app.app_context():
        initialize_database(app)
    
    return app


