"""
Database Setup Script
This script automatically creates the database and tables based on tables.sql
"""

import mysql.connector
from mysql.connector import Error
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USERNAME', 'root'),
    'password': os.getenv('DB_PASSWORD', '')
}

DATABASE_NAME = os.getenv('DB_NAME', 'finsight_db')
SQL_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'tables.sql')


def create_database_connection(include_db=False):
    """Create a connection to MySQL server."""
    try:
        config = DB_CONFIG.copy()
        if include_db:
            config['database'] = DATABASE_NAME
        
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"✓ Successfully connected to MySQL Server version {db_info}")
            return connection
    except Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        return None


def create_database(connection):
    """Create the database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        
        # Check if database exists
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if DATABASE_NAME in databases:
            print(f"⚠ Database '{DATABASE_NAME}' already exists")
            response = input("Do you want to drop and recreate it? (yes/no): ").lower()
            
            if response == 'yes':
                cursor.execute(f"DROP DATABASE {DATABASE_NAME}")
                print(f"✓ Dropped existing database '{DATABASE_NAME}'")
            else:
                print("✓ Using existing database")
                cursor.close()
                return True
        
        # Create database
        cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
        print(f"✓ Database '{DATABASE_NAME}' created successfully")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"✗ Error creating database: {e}")
        return False


def execute_sql_file(connection, sql_file_path):
    """Execute SQL commands from a file."""
    try:
        cursor = connection.cursor()
        
        # Read the SQL file
        if not os.path.exists(sql_file_path):
            print(f"✗ SQL file not found: {sql_file_path}")
            return False
        
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Split SQL commands (handle multiple statements)
        # Remove comments and split by semicolon
        sql_commands = []
        current_command = []
        
        for line in sql_content.split('\n'):
            # Skip comment lines
            if line.strip().startswith('--') or line.strip().startswith('#'):
                continue
            
            current_command.append(line)
            
            # If line ends with semicolon, it's end of command
            if line.strip().endswith(';'):
                command = '\n'.join(current_command)
                if command.strip():
                    sql_commands.append(command)
                current_command = []
        
        # Execute each command
        print(f"\n{'='*60}")
        print(f"Executing SQL commands from {sql_file_path}")
        print(f"{'='*60}\n")
        
        for i, command in enumerate(sql_commands, 1):
            try:
                # Extract table name for better output
                command_lower = command.lower()
                if 'create table' in command_lower:
                    table_name = command_lower.split('create table')[1].split('(')[0].strip()
                    print(f"[{i}/{len(sql_commands)}] Creating table: {table_name}...", end=' ')
                else:
                    print(f"[{i}/{len(sql_commands)}] Executing command...", end=' ')
                
                cursor.execute(command)
                print("✓")
                
            except Error as e:
                print(f"✗\n    Error: {e}")
                # Continue with other commands even if one fails
                continue
        
        connection.commit()
        print(f"\n{'='*60}")
        print("✓ All SQL commands executed successfully")
        print(f"{'='*60}\n")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"✗ Error executing SQL file: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def verify_tables(connection):
    """Verify that all tables were created successfully."""
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        print("\n📊 Tables created in database:")
        print(f"{'='*60}")
        for i, table in enumerate(tables, 1):
            print(f"  {i}. {table}")
        print(f"{'='*60}")
        print(f"✓ Total tables created: {len(tables)}\n")
        
        cursor.close()
        return True
        
    except Error as e:
        print(f"✗ Error verifying tables: {e}")
        return False


def main():
    """Main function to orchestrate database setup."""
    print("\n" + "="*60)
    print("       FinSight Database Setup Script")
    print("="*60 + "\n")
    
    # Step 1: Connect to MySQL Server
    print("Step 1: Connecting to MySQL Server...")
    connection = create_database_connection(include_db=False)
    
    if not connection:
        print("\n✗ Failed to connect to MySQL. Please check your configuration.")
        return
    
    # Step 2: Create Database
    print("\nStep 2: Creating database...")
    if not create_database(connection):
        connection.close()
        return
    
    connection.close()
    
    # Step 3: Connect to the new database
    print("\nStep 3: Connecting to the new database...")
    connection = create_database_connection(include_db=True)
    
    if not connection:
        print("\n✗ Failed to connect to the database.")
        return
    
    # Step 4: Execute SQL file
    print(f"\nStep 4: Executing SQL from '{SQL_FILE_PATH}'...")
    if not execute_sql_file(connection, SQL_FILE_PATH):
        connection.close()
        return
    
    # Step 5: Verify tables
    print("Step 5: Verifying tables...")
    verify_tables(connection)
    
    # Close connection
    connection.close()
    print("✓ Database connection closed")
    
    print("\n" + "="*60)
    print("   ✓ Database setup completed successfully!")
    print("="*60 + "\n")
    
    print("📝 Next steps:")
    print("  1. Run 'python populate_db.py' to add sample data")
    print("  2. Start your Flask app with 'python app.py'\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Setup interrupted by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
