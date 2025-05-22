import time
import sqlite3 
import functools
from contextlib import contextmanager

# Database connection decorator
def with_db_connection(func):
    """Decorator for handling database connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

# Retry decorator
def retry_on_failure(retries=3, delay=2):
    """Decorator that retries database operations on failure"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (sqlite3.OperationalError, sqlite3.InterfaceError) as e:
                    last_exception = e
                    if attempt < retries - 1:  # Don't sleep on last attempt
                        print(f"Attempt {attempt + 1} failed, retrying in {delay} seconds...")
                        time.sleep(delay)
                    continue
                except Exception as e:
                    # Don't retry on non-transient errors
                    print(f"Non-retryable error: {e}")
                    raise
            
            print(f"All {retries} attempts failed")
            raise last_exception if last_exception else Exception("Unknown error")
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
if __name__ == "__main__":
    try:
        users = fetch_users_with_retry()
        print(users)
    except Exception as e:
        print(f"Failed to fetch users after retries: {e}")