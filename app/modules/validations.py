import re

def is_valid_email(email):
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def is_valid_password(password):
    """Validate password format"""
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.match(pattern, password))

def is_valid_phone(phone):
    """Validate phone number format (10 digits)"""
    pattern = r"^\d{10}$"
    return bool(re.match(pattern, phone))

def is_valid_username(username):
    """Validate username format (alphanumeric, 3-15 characters)"""
    pattern = r"^[a-zA-Z0-9]{3,30}$"
    return bool(re.match(pattern, username))

def is_valid_department(department):
    """Validate department selection (non-empty)"""
    return bool(department)

def is_valid_role(role):
    """Validate role selection (non-empty)"""
    return bool(role)
