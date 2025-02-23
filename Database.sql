import sqlite3

# Database filename
DB_FILENAME = "climbing_gym.db"

# SQL commands to create tables
CREATE_TABLES_SQL = """
-- Create the gyms table
CREATE TABLE IF NOT EXISTS gyms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Create the sectors table
CREATE TABLE IF NOT EXISTS sectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gym_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (gym_id) REFERENCES gyms(id) ON DELETE CASCADE
);

-- Create the setters table
CREATE TABLE IF NOT EXISTS setters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Create the climbs table (Active climbs)
CREATE TABLE IF NOT EXISTS climbs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_id INTEGER NOT NULL,
    setter_id INTEGER NOT NULL,
    color TEXT NOT NULL,
    grade TEXT NOT NULL,
    date_set DATE NOT NULL,
    FOREIGN KEY (sector_id) REFERENCES sectors(id) ON DELETE CASCADE,
    FOREIGN KEY (setter_id) REFERENCES setters(id) ON DELETE CASCADE
);

-- Create the climb_archive table (Stores removed climbs)
CREATE TABLE IF NOT EXISTS climb_archive (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gym_id INTEGER NOT NULL,
    climb_id INTEGER NOT NULL,
    sector_id INTEGER NOT NULL,
    setter_id INTEGER NOT NULL,
    color TEXT NOT NULL,
    grade TEXT NOT NULL,
    date_set DATE NOT NULL,
    date_removed DATE NOT NULL,
    FOREIGN KEY (gym_id) REFERENCES gyms(id) ON DELETE CASCADE,
    FOREIGN KEY (climb_id) REFERENCES climbs(id) ON DELETE CASCADE,
    FOREIGN KEY (sector_id) REFERENCES sectors(id) ON DELETE CASCADE,
    FOREIGN KEY (setter_id) REFERENCES setters(id) ON DELETE CASCADE
);
"""

def initialize_database():
    """Creates the SQLite database and tables."""
    try:
        conn = sqlite3.connect(DB_FILENAME)  # Connect to (or create) database
        cursor = conn.cursor()
        cursor.executescript(CREATE_TABLES_SQL)  # Run SQL script
        conn.commit()  # Save changes
        conn.close()  # Close connection
        print("✅ Database initialized successfully!")
    except sqlite3.Error as e:
        print(f"❌ Error initializing database: {e}")

if __name__ == "__main__":
    initialize_database()
