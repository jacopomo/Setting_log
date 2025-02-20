import sqlite3
from datetime import date

# Database filename
DB_FILENAME = "climbing_gym.db"

# Sample data to insert
gyms = [
    ('ClimbO',),
    ('Apuano Appeso',)
]

sectors = [
    (1, 'Placca shop'),
    (1, 'Placca sx'),
    (1, 'Tetto sx'),
    (1, 'Tetto sotto'),
    (1, 'Tetto dx'),
    (1, 'Placca dx'),
    (1, '5 gradi'),
    (1, 'Diedro sx'),
    (1, '15 gradi'),
    (1, 'Strapiombo'),
    (1, 'Diedro dx'),
    (1, 'Spray'),
    (1, 'Comp'),
    (2, 'Placca sx'),
    (2, 'Diedro sx'),
    (2, '10 gradi'),
    (2, 'Srapiombo'), 
    (2, '15 gradi'),
    (2, 'Diedro dx'),
    (2, 'Placca dx')
]

setters = [
    ('Jacopo Omodei',),
    ('Ruggero Collavini',),
    ('Leonardo Bellinvia',),
    ('Pietro Del Rio',),
    ('Andrea Baroncini',)
]

climbs = [
    (1, 1, 'Verde', '3', '2025-02-20'),
    (1, 2, 'Giallo', '4', '2025-02-02'),
    (2, 1, 'Blu', '8', '2025-01-12'),
    (2, 2, 'Giallo', '7', '2025-01-12')
]

def insert_sample_data():
    """Inserts sample data into the database."""
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()

        # Insert gyms
        cursor.executemany("INSERT INTO gyms (name) VALUES (?)", gyms)

        # Insert sectors
        cursor.executemany("INSERT INTO sectors (gym_id, name) VALUES (?, ?)", sectors)

        # Insert setters
        cursor.executemany("INSERT INTO setters (name) VALUES (?)", setters)

        # Insert climbs
        cursor.executemany("INSERT INTO climbs (sector_id, setter_id, color, grade, date_set) VALUES (?, ?, ?, ?, ?)", climbs)

        conn.commit()
        conn.close()

        print("✅ Sample data inserted successfully!")
    except sqlite3.Error as e:
        print(f"❌ Error inserting data: {e}")

if __name__ == "__main__":
    insert_sample_data()
