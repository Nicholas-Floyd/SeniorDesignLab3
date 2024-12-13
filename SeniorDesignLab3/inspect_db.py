import sqlite3

def inspect_db():
    db_path = "SeniorDesignLab3/instance/flaskr.sqlite"  # Update the path if needed
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # List all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tables in the database:")
        for table in tables:
            print(f"- {table[0]}")

        # Check contents of the `users` table (if it exists)
        if any(table[0] == 'users' for table in tables):
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            print("\nUsers table content:")
            for user in users:
                print(user)
        else:
            print("\nThe `users` table does not exist.")

        conn.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_db()
