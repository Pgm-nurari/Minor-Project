from pocketbase import PocketBase
from pocketbase.client import FileUpload

client = PocketBase('https://finsight.pockethost.io/')

# Authenticate as regular user
try:
    user_data = client.collection("users").auth_with_password("mrprogrammer5879@gmail.com", "1234567890")
    print("User authenticated:", user_data.is_valid)
except Exception as e:
    print("User authentication failed:", str(e))

try:
    # Fetch records without any filter to see if it works
    result = client.collection("users").get_list(1, 20)
    print("Records fetched:", result)
except Exception as e:
    print("Error fetching records:", str(e))
    if hasattr(e, 'response'):
        print("Response body:", e.response.text)

# Create record and upload file to image field
# try:
#     with open("image.png", "rb") as img:
#         result = client.collection("users").create(
#             {
#                 "status": True,  # Use True instead of "true"
#                 "image": FileUpload(("image.png", img)),
#             }
#         )
#         print("Record created:", result)
# except Exception as e:
#     print("Error creating record:", str(e))

# For adding records into 'users' collection...!
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

# try:
    #     # Create a new record in the 'users' collection
    #     record = client.collection('users').create(data)
    #     print("Record created:", record)

    #     # (optional) send an email verification request
    #     # verification_response = client.collection('users').request_verification('test@example.com')
    #     # print("Verification request sent:", verification_response)
    # except Exception as e:
    #     print("Error:", str(e))

    # try:
    #     # Fetch all user records
    #     users_result = client.collection("users").get_list(1, 100)  # Adjust the page and limit as needed
    #     users = users_result.items  # Get the list of user records
    # except Exception as e:
    #     print("Error fetching users:", str(e))
    #     users = []  # Default to an empty list if there's an error
    
# Authenticate as admin
    # try:
    #     admin_data = client.admins.auth_with_password("hackerrank123sab@gmail.com", "123@hack#sab")
    #     print("Admin authenticated:", admin_data.is_valid)
    # except Exception as e:
    #     print("Admin authentication failed:", str(e))      