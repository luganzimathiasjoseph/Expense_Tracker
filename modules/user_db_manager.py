import sqlite3

# SQLite database file
DB_PATH = "database/user.db"


def init_db():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create the 'users' table if it doesn't exist
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Insert default user data if it doesn't already exist
    cursor.execute(''' 
        INSERT OR IGNORE INTO users (username, password) 
        VALUES (?, ?) 
    ''', ('user', 'admin'))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()


# Function to get the stored password for a user 
def get_user_password(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        stored_password = cursor.fetchone()
        return stored_password[0] if stored_password else None
    finally:
        conn.close()


# Function to get all user details 
def get_users():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM users")  
        users = cursor.fetchall()  
        if users:
            # Convert the result to a list of dictionaries
            return [{'id': user[0], 'username': user[1], 'password': user[2]} for user in users]
        return [] 
    finally:
        conn.close()



# Function to authenticate user credentials 
def authenticate_user(username, password):
    try:
        stored_password = get_user_password(username)
        if stored_password:
            return stored_password == password  
        return False
    except Exception as e:
        return False 


# Function to add a new user to the database
def add_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        if get_user_password(username):  # Check if user already exists
            return False

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    finally:
        conn.close()


# Function to change the username and/or password of a user
def change_credentials(old_username, old_password, new_username, new_password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Verify the old credentials
        stored_password = get_user_password(old_username)
        if stored_password and stored_password == old_password:
            # Delete the old user record
            cursor.execute("DELETE FROM users WHERE username = ?", (old_username,))
            conn.commit()
            # Add the new credentials
            return add_user(new_username, new_password)
        return False
    finally:
        conn.close()

# Initialize the database 
init_db()
