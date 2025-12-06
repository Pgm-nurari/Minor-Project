from app import create_app, db
from app.modules.models import User, Role
from werkzeug.security import check_password_hash

app = create_app()

with app.app_context():
    # Check admin user
    admin = User.query.filter_by(Email='admin@finsight.com').first()
    
    if admin:
        print("="*60)
        print("ADMIN USER DETAILS")
        print("="*60)
        print(f"Email: {admin.Email}")
        print(f"Username: {admin.Username}")
        print(f"Role ID: {admin.Role}")
        print(f"Department ID: {admin.Dept_ID}")
        print(f"Verified: {admin.Verified}")
        print(f"Password Hash: {admin.Password[:50]}...")
        
        # Check role
        role = Role.query.filter_by(Role_ID=admin.Role).first()
        print(f"Role Name: {role.Role_Name if role else 'NOT FOUND'}")
        
        # Test password
        test_password = "Password@123"
        password_matches = check_password_hash(admin.Password, test_password)
        print(f"\nPassword 'Password@123' matches: {password_matches}")
        
        print("="*60)
    else:
        print("❌ Admin user NOT found!")
        
    # List all roles
    print("\nALL ROLES:")
    roles = Role.query.all()
    for role in roles:
        print(f"  Role ID {role.Role_ID}: {role.Role_Name}")
    
    # List all users
    print("\nALL USERS:")
    users = User.query.all()
    for user in users:
        role = Role.query.filter_by(Role_ID=user.Role).first()
        print(f"  {user.Email} - Role: {role.Role_Name if role else 'Unknown'} - Verified: {user.Verified}")
