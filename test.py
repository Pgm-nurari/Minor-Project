import mysql.connector
from mysql.connector import Error

def connect_and_read():
    try:
        # Establish the connection
        connection = mysql.connector.connect(
            host="localhost",
            user="finsight_user",            # Replace with your MySQL username
            password="finsight10466266",  # Replace with your MySQL password
            database="finsight_db"            # Replace with your database name
        )

        if connection.is_connected():
            print("Connected to MySQL database")

            # Create a cursor and execute a query
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM test")
            

            # Fetch all rows from the executed query
            rows = cursor.fetchall()

            print("Data from test table:")
            for row in rows:
                print(row)  # Each row is a tuple (id, name, age)

    except Error as e:
        print("Error connecting to MySQL:", e)

    finally:
        # Close the connection
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed")

# Run the function
connect_and_read()
