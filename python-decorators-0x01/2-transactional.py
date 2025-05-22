import sqlite3 
import functools
from contextlib import contextmanager

# Context manager for DB connections
@contextmanager
def with_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Transaction manager decorator
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed successfully")
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise
    return wrapper

@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Updated email for user {user_id}")

# only one call inside the context manager
if __name__ == "__main__":
    with with_db_connection() as conn:
        update_user_email(conn, user_id=1, new_email='Crawford_Cartwright@hotmail.com')