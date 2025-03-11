import sqlite3

# Database filename
DB_FILENAME = "climbing_gym.db"

# Sample data
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
    (2, 'Strapiombo'), 
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

# Define grading schemes per gym
grades = [
    (1, 'Verde'),
    (1, 'Blu'),
    (1, 'Giallo'),
    (1, 'Arancione'),
    (1, 'Rosso'),
    (1, 'Viola'),
    (2, '1'),
    (2, '2'),
    (2, '3'),
    (2, '4'),
    (2, '5'),
    (2, '6'),
    (2, '7'),
    (2, '8'),
    (2, '9')
]

# Sample climbs with grade reference
climbs = [
    (1, 1, 'Verde', 1, '2025-02-20'),  # Uses grade_id 1 (Verde for ClimbO)
    (1, 2, 'Giallo', 3, '2025-02-02'), # Uses grade_id 3 (Giallo for ClimbO)
    (2, 1, 'Blu', 8, '2025-01-12'),    # Uses grade_id 8 (Grade '8' for Apuano Appeso)
    (2, 2, 'Giallo', 7, '2025-01-12')  # Uses grade_id 7 (Grade '7' for Apuano Appeso)
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

        # Insert grades
        cursor.executemany("INSERT INTO grades (gym_id, grade) VALUES (?, ?)", grades)

        # Insert climbs (now referencing grade_id)
        cursor.executemany("INSERT INTO climbs (sector_id, setter_id, color, grade_id, date_set) VALUES (?, ?, ?, ?, ?)", climbs)

        conn.commit()
        conn.close()

        print("✅ Sample data inserted successfully!")
    except sqlite3.Error as e:
        print(f"❌ Error inserting data: {e}")

if __name__ == "__main__":
    insert_sample_data()
