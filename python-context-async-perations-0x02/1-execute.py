import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
    
    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor
    
    def __exit__(self, type, value, traceback):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        # Handle exceptions if they occurred
        if type:
            print(f"Query execution error: {value}")
        return False


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    
    with ExecuteQuery('users.db', query, params) as cursor:
        results = cursor.fetchall()
        print("Users over 25 years old:")
        for row in results:
            print(dict(row))