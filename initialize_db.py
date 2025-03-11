import sqlite3

DB_FILENAME = "climbing_gym.db"

# Read the SQL script with UTF-8 encoding
with open("Database.sql", "r", encoding="utf-8") as f:
    sql_script = f.read()

# Execute the script
try:
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")
except sqlite3.Error as e:
    print(f"❌ Error initializing database: {e}")
