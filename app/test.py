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