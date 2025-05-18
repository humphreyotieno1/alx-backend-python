import csv
import uuid
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# connecting to the database
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.environ.get('DB_PASSWORD')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
# creating a database
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database created successfully")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        if cursor:
            cursor.close()
            
# connect to the database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.environ.get('DB_PASSWORD'),
            database='ALX_prodev'
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
# creating a table
def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(10, 0) NOT NULL,
                INDEX (user_id)
            )
        """)
        print("Table created successfully")
    except Error as e:
        print(f"Error creating table: {e}")
    finally:
        if cursor:
            cursor.close()
            
# inserting data into the table
def insert_data(connection, data):
    try:
        cursor = connection.cursor()
            
        for row in data:
            cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (row['user_id'],))
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (row['user_id'], row['name'], row['email'], row['age']))
                    
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")
        connection.rollback()
    finally:
        if cursor:
            cursor.close()
            
def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Connect to MySQL server
    connection = connect_db()
    if not connection:
        print("Failed to connect to MySQL server. Exiting...")
        return
    
    # Create database
    create_database(connection)
    connection.close()
    
    # Connect to the ALX_prodev database
    prodev_connection = connect_to_prodev()
    if not prodev_connection:
        print("Failed to connect to ALX_prodev database. Exiting...")
        return
    
    # Create table
    create_table(prodev_connection)
    
    # Read data from CSV file (if available) or create sample data
    try:
        data = []
        csv_file = 'user_data.csv'
        
        if os.path.exists(csv_file):
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    data.append({
                        'user_id': row.get('user_id', str(uuid.uuid4())),
                        'name': row['name'],
                        'email': row['email'],
                        'age': row['age']
                    })
        else:
            print(f"CSV file {csv_file} not found. Generating sample data.")
        
        # Insert data
        insert_data(prodev_connection, data)
    except Exception as e:
        print(f"Error processing data: {e}")
    finally:
        if prodev_connection:
            prodev_connection.close()
            print("Database connection closed")

if __name__ == "__main__":
    main()
