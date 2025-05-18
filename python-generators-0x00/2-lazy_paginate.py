import sys
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# connect to database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = os.environ.get('DB_PASSWORD'),
            database = 'ALX_prodev'
        )
        return connection
    except Error as e: 
        print(f"Error connecting to MySQL: {e}")
        return None

# paginate through the user data in the database.
def paginate_users(page_size, offset):
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        if not connection:
            raise []

        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
        return rows

    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
# lazy load the user data in the database.
def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
        
if __name__ == "__main__":
    try:
        for page in lazy_paginate(100):
            for user in page:
                print(user)
    except BrokenPipeError:
        sys.stderr.close()