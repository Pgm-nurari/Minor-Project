import re

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def is_valid_password(password):
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.match(pattern, password))

def is_valid_phone(phone):
    pattern = r"^\d{10}$"  
    return bool(re.match(pattern, phone))

def is_valid_username(username):
    pattern = r"^[a-zA-Z0-9]{3,15}$"  # Only alphanumeric, 3-15 characters
    return bool(re.match(pattern, username))
# def main():
#     pass

# if __name__=='__main__':
#     main()
