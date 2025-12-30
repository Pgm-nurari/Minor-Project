"""
FinSight - Financial Event Management System
Startup Script

This script:
1. Checks Python dependencies
2. Creates database and tables automatically if they don't exist
3. Starts the Flask development server
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required packages are installed"""
    print("="*60)
    print("Checking dependencies...")
    print("="*60)
    
    try:
        import flask
        import flask_sqlalchemy
        import mysql.connector
        import werkzeug
        print("✓ All required packages are installed\n")
        return True
    except ImportError as e:
        print(f"✗ Missing package: {e}")
        print("\n📦 Installing dependencies from requirements.txt...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✓ Dependencies installed successfully\n")
            return True
        except Exception as install_error:
            print(f"✗ Failed to install dependencies: {install_error}")
            print("\nPlease run manually: pip install -r requirements.txt")
            return False

def main():
    print("\n" + "="*60)
    print("       FinSight - Financial Event Management")
    print("="*60 + "\n")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if database has data
    print("="*60)
    print("Starting application...")
    print("="*60)
    
    # Import and run the app
    from app import create_app
    
    app = create_app('development')
    
    print("\n" + "="*60)
    print("✓ Application started successfully!")
    print("="*60)
    print("\n📱 Access the application at: http://127.0.0.1:5000")
    print("\n👤 Default login credentials:")
    print("   Admin: admin@finsight.com / Password@123")
    print("   Event Manager: john.doe@finsight.com / Password@123")
    print("   Finance Manager: jane.smith@finsight.com / Password@123")
    print("\n⚠  Note: If this is your first run with an empty database,")
    print("   run 'python scripts/populate_db.py' to add sample data")
    print("\n" + "="*60 + "\n")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
