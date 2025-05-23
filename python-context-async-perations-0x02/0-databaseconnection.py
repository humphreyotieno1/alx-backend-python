import sqlite3

class DatabaseConnection:
    def __init__(self, dbName):
        self.dbName = dbName
        self.conn = None
        
    # Open connection
    def __enter__(self):
        self.conn = sqlite3.connect(self.dbName)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    # Close connection
    def __exit__(self, type, value, traceback):
        if self.conn:
            self.conn.close()
            
        if type:
            print(f"Error occured: {value}")
            return False
        
if __name__ == "__main__":
    with DatabaseConnection('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        
        print("Users in DB")
        for row in results:
            print(dict(row))