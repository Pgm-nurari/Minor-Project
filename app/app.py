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

# Authenticate as admin
try:
    admin_data = client.admins.auth_with_password("hackerrank123sab@gmail.com", "123@hack#sab")
    print("Admin authenticated:", admin_data.is_valid)
except Exception as e:
    print("Admin authentication failed:", str(e))

# data = {
#     "username": "nurari",
#     "email": "nurarisab6453@gmail.com",
#     "emailVisibility": True,
#     "password": "12345678",
#     "passwordConfirm": "12345678",
#     "name": "nurari"
# }

# try:
#     # Create a new record in the 'users' collection
#     record = client.collection('users').create(data)
#     print("Record created:", record)

#     # (optional) send an email verification request
#     # verification_response = client.collection('users').request_verification(data["email"])
#     # print("Verification request sent:", verification_response)
# except Exception as e:
#     print("Error:", str(e))

    

@app.route('/')
def home():
    # try:
    #     # Create a new record in the 'users' collection
    #     record = client.collection('users').create(data)
    #     print("Record created:", record)

    #     # (optional) send an email verification request
    #     # verification_response = client.collection('users').request_verification('test@example.com')
    #     # print("Verification request sent:", verification_response)
    # except Exception as e:
    #     print("Error:", str(e))

    try:
        # Fetch all user records
        users_result = client.collection("users").get_list(1, 100)  # Adjust the page and limit as needed
        users = users_result.items  # Get the list of user records
    except Exception as e:
        print("Error fetching users:", str(e))
        users = []  # Default to an empty list if there's an error

    return render_template('index.html', users=users)  # Pass users data to the template

if __name__ == '__main__':
    app.run(debug=True)
