import sqlite3

# Connect (this creates users.db automatically)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Insert default admin user
cursor.execute("""
INSERT INTO users (username, password)
VALUES (?, ?)
""", ("admin", "1234"))

conn.commit()
conn.close()

print("users.db created successfully and admin user added!")
