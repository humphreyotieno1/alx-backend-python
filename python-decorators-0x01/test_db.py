import sqlite3
from contextlib import closing

# database initialisation
def init_db():
    with closing(sqlite3.connect('users.db')) as conn:
        with conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    age INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Data insertion
            cursor.executemany(
                "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
                [
                    ('alice', 'alice@example.com', 28),
                    ('bob', 'bob@example.com', 32),
                    ('charlie', 'charlie@example.com', 25),
                    ('diana', 'diana@example.com', 41)
                ]                   
            )
            print(f"Database initialised with sample data")

if __name__ == '__main__':
    init_db()