import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

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
    
# generator to fetch rows one by one
def stream_users():
    connection = None
    cursor = None
    try:
        load_dotenv()
        connection = connect_to_prodev()
        if not connection:
            raise StopIteration
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
    except Error as e:
        print(f"Error fetching data: {e}")
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
def main():
    for user in stream_users():
        print(user)
        
if __name__ == "__main__":
    main()
        