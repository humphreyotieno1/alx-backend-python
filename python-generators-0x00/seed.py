import csv
import uuid
import mysql.connector
from mysql.connector import Error
import os

# connecting to the database
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.env.DB_PASSWORD
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
        print("Dtabase created successfully")
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
            password=os.env.DB_PASSWORD,
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