import sqlite3
from werkzeug.security import generate_password_hash

def update_password(username, new_password):
    db = sqlite3.connect('instance/flaskr.sqlite')  
    hashed_password = generate_password_hash(new_password)
    db.execute('UPDATE users SET password = ? WHERE username = ?', (hashed_password, username))
    db.commit()
    db.close()
    print(f"Password for {username} has been updated.")

if __name__ == "__main__":
    user = input("Enter username: ")
    new_pass = input("Enter new password: ")
    update_password(user, new_pass)
