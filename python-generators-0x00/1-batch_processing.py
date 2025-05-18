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
    
# generator to fetch rows in batches
def stream_users_in_batches(batch_size):
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
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
            
    except Error as e:
        print(f"Error fetching data: {e}")
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            
# function to process each batch
def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        filtered_users = [user for user in batch if user['age'] > 25]
        for user in filtered_users:
            print(user)
            
if __name__ == "__main__":
    import sys
    try:
        batch_processing(50)
    except BrokenPipeError:
        sys.stderr.close()