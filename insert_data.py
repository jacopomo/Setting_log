import sqlite3

# Database filename
DB_FILENAME = "climbing_gym.db"

# Sample data

# (name, map_path)
mapfolder = '/static/gym_maps/'
gyms = [
    ('ClimbO',mapfolder+'ClimbO_map.png'),      #id 1
    ('Apuano Appeso',mapfolder+'AA_map.png')    #id 2
]

# (gym_id, sector_id, name, x, y)
sectors = [
#CLIMBO
    (1, 'Placca shop', 100, 150),        # Sector 1 for gym 1
    (1, 'Placca sx', 200, 250),          # Sector 2 for gym 1
    (1, 'Tetto sx', 150, 200),           # Sector 3 for gym 1
    (1, 'Tetto sotto', 400, 500),        # Sector 4 for gym 1
    (1, 'Tetto dx', 450, 550),           # Sector 5 for gym 1
    (1, 'Placca dx', 350, 400),          # Sector 6 for gym 1
    (1, '5 gradi', 250, 300),            # Sector 7 for gym 1
    (1, 'Diedro sx', 300, 350),          # Sector 8 for gym 1
    (1, '15 gradi', 600, 700),           # Sector 9 for gym 1
    (1, 'Strapiombo', 700, 750),        # Sector 10 for gym 1
    (1, 'Diedro dx', 450, 400),         # Sector 11 for gym 1
    (1, 'Spray', 550, 650),             # Sector 12 for gym 1
    (1, 'Comp', 650, 700),              # Sector 13 for gym 1
#APUANO APPESO
    (2, 'Placca sx', 250, 300),          # Sector 1 for gym 2
    (2, 'Diedro sx', 350, 400),          # Sector 2 for gym 2
    (2, '10 gradi', 300, 350),           # Sector 3 for gym 2
    (2, 'Strapiombo', 450, 500),         # Sector 4 for gym 2
    (2, '15 gradi', 550, 600),           # Sector 5 for gym 2
    (2, 'Diedro dx', 600, 650),          # Sector 6 for gym 2
    (2, 'Placca dx', 500, 550)           # Sector 7 for gym 2
]


setters = [
    ('Jacopo Omodei',),                 #id 1
    ('Ruggero Collavini',),             #id 2
    ('Leonardo Bellinvia',),            #id 3
    ('Pietro Del Rio',),                #id 4
    ('Andrea Baroncini',)               #id 5
]

# Define grading schemes per gym
grades = [
#CLIMBO
    (1, 'Verde'),                       #Grade 1 for gym 1
    (1, 'Blu'),                         #Grade 2 for gym 1                
    (1, 'Giallo'),                      #Grade 3 for gym 1
    (1, 'Arancione'),                   #Grade 4 for gym 1
    (1, 'Rosso'),                       #Grade 5 for gym 1
    (1, 'Viola'),                       #Grade 6 for gym 1
#APUANO APPESO
    (2, '1'),                           #Grade 1 for gym 2
    (2, '2'),                           #Grade 2 for gym 2
    (2, '3'),                           #Grade 3 for gym 2
    (2, '4'),                           #Grade 4 for gym 2
    (2, '5'),                           #Grade 5 for gym 2
    (2, '6'),                           #Grade 6 for gym 2
    (2, '7'),                           #Grade 7 for gym 2
    (2, '8'),                           #Grade 8 for gym 2
    (2, '9')                            #Grade 9 for gym 2
]

# Sample climbs with grade reference
# (gym_id, sector_id, setter_id, color, grade_id, date_set)
climbs = [
    (1, 1, 1, 'Verde', 3, '2025-02-20'),        # Gym 1, Sector 1, Setter 1, Green, Grade 3, Date set: 2025-02-20
    (1, 10, 4, 'Arancione', 6, '2025-02-02'),   # Gym 1, Sector 10, Setter 4, Orange, Grade 6, Date set: 2025-02-02
    (2, 3, 2, 'Blu', 8, '2025-01-12'),          # Gym 2, Sector 3, Setter 2, Blue, Grade 8, Date set: 2025-01-12
    (2, 6, 3, 'Giallo', 7, '2025-01-12')        # Gym 2, Sector 6, Setter 3, Yellow, Grade 7, Date set: 2025-01-12
]

def insert_sample_data():
    """Inserts sample data into the database."""
    try:
        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()

        # Enable foreign keys
        cursor.execute('PRAGMA foreign_keys = ON')

        # Insert gyms
        cursor.executemany("INSERT INTO gyms (name, map_path) VALUES (?, ?)", gyms)

        # Insert sectors
        cursor.executemany("INSERT INTO sectors (gym_id, name, x, y) VALUES (?, ?, ?, ?)", sectors)

        # Insert setters
        cursor.executemany("INSERT INTO setters (name) VALUES (?)", setters)

        # Insert grades
        cursor.executemany("INSERT INTO grades (gym_id, grade) VALUES (?, ?)", grades)

        # Insert climbs
        cursor.executemany("INSERT INTO climbs (gym_id, sector_id, setter_id, color, grade_id, date_set) VALUES (?, ?, ?, ?, ?, ?)", climbs)

        conn.commit()
        conn.close()

        print("✅ Sample data inserted successfully!")
    except sqlite3.Error as e:
        print(f"❌ Error inserting data: {e}")

if __name__ == "__main__":
    insert_sample_data()
