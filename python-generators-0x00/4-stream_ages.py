import sys
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

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
    
# stream ages from the database one by one
def stream_user_ages():
    connection = None
    cursor = None
    try:
        connection = connect_to_prodev()
        if not connection:
            return
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row['age']
            
    except Error as e:
        print(f"Error fetching data: {e}")
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()