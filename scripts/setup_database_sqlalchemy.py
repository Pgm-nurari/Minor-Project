"""
Alternative Database Setup using SQLAlchemy Models
This script creates tables using the SQLAlchemy ORM models defined in the application
"""

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.modules.models import *
import mysql.connector
from mysql.connector import Error


def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'mysql123!@#MYSQL'
    }
    
    DATABASE_NAME = 'finsight_db'
    
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Check if database exists
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if DATABASE_NAME in databases:
                print(f"✓ Database '{DATABASE_NAME}' already exists")
            else:
                cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
                print(f"✓ Database '{DATABASE_NAME}' created successfully")
            
            cursor.close()
            connection.close()
            return True
            
    except Error as e:
        print(f"✗ Error: {e}")
        return False


def setup_database_with_sqlalchemy():
    """Create all tables using SQLAlchemy models."""
    print("\n" + "="*60)
    print("   FinSight Database Setup (SQLAlchemy Method)")
    print("="*60 + "\n")
    
    # Step 1: Create database
    print("Step 1: Creating database...")
    if not create_database_if_not_exists():
        return
    
    # Step 2: Initialize Flask app
    print("\nStep 2: Initializing Flask application...")
    app = create_app()
    
    # Step 3: Create tables
    print("\nStep 3: Creating tables from SQLAlchemy models...")
    with app.app_context():
        try:
            # Drop all tables (optional - be careful!)
            response = input("Drop existing tables? (yes/no): ").lower()
            if response == 'yes':
                print("⚠ Dropping all existing tables...")
                db.drop_all()
                print("✓ Tables dropped")
            
            # Create all tables
            print("Creating tables...")
            db.create_all()
            
            # Verify tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            table_names = inspector.get_table_names()
            
            print("\n📊 Tables created:")
            print("="*60)
            for i, table in enumerate(table_names, 1):
                print(f"  {i}. {table}")
            print("="*60)
            print(f"✓ Total tables: {len(table_names)}\n")
            
            print("\n" + "="*60)
            print("   ✓ Database setup completed successfully!")
            print("="*60 + "\n")
            
            print("📝 Next steps:")
            print("  1. Run 'python populate_db.py' to add sample data")
            print("  2. Start your Flask app with 'python app.py'\n")
            
        except Exception as e:
            print(f"✗ Error creating tables: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    try:
        setup_database_with_sqlalchemy()
    except KeyboardInterrupt:
        print("\n\n⚠ Setup interrupted by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
