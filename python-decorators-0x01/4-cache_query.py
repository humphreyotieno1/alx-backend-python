import time
import sqlite3 
import functools
from contextlib import contextmanager

# Query cache dictionary
query_cache = {}

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

# Query caching decorator
def cache_query(func):
    """Decorator that caches query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Create a cache key from the query and parameters
        cache_key = (query, tuple(kwargs.items()))
        
        # Check cache first
        if cache_key in query_cache:
            print("Returning cached results")
            return query_cache[cache_key]
        
        # Execute and cache if not found
        result = func(conn, query, *args, **kwargs)
        query_cache[cache_key] = result
        print("Caching new results")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users from database with query caching"""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    print("First call (will execute query and cache results):")
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Fetched {len(users)} users")
    
    print("\nSecond call (will use cached results):")
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(f"Fetched {len(users_again)} users from cache")