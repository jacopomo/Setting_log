import sqlite3

def insert_data():
    conn = sqlite3.connect("climbing_gym.db")
    cursor = conn.cursor()

    # Insert gyms
    gyms = [
        ("ClimbO", "/static/gym_maps/ClimbO_map.png"),
        ("Apuano Appeso", "/static/gym_maps/Apuano_map.png"),
        ("Farm", "/static/gym_maps/Farm_map.png")
    ]
    cursor.executemany("INSERT INTO gyms (name, map_location) VALUES (?, ?) ON CONFLICT(name) DO NOTHING;", gyms)

    # Insert setters
    setters = ["Jacopo", "Leo", "Rugo", "Pietro", "Baro"]
    cursor.executemany("INSERT INTO setters (name) VALUES (?) ON CONFLICT(name) DO NOTHING;", [(s,) for s in setters])

    # Insert sectors with estimated coordinates
    sectors = {
        "ClimbO": [
            ("placca shop", 300, 100, "[(280,90), (320,110)]"),
            ("tetto", 450, 120, "[(430,110), (470,130)]"),
            ("diedro", 600, 150, "[(580,140), (620,160)]"),
            ("strapiombo", 750, 180, "[(730,170), (770,190)]"),
            ("spray", 850, 200, "[(830,190), (870,210)]")
        ],
        "Apuano Appeso": [
            ("Diedro sx", 177, 105, "[(177,142), (177,60), (205,60)]"),
            ("10 gradi", 264, 64, "[(206,60),(350, 60)]"),
            ("Strapiombo", 458, 124, "[(351,63), (425,124), (566,166)]"),
            ("15 gradi", 596, 88, "[(567,166), (618,71)]"),
            ("Diedro dx", 652, 80, "[(619,71), (654,50), (657,118)]"),
            ("Placca", 660, 200, "[(657,119), (659,316)]")
        ],
        "Farm": [
            ("placca", 200, 100, "[(180,90), (220,110)]"),
            ("grotta", 400, 130, "[(380,120), (420,140)]"),
            ("fungo", 600, 160, "[(580,150), (620,170)]"),
            ("comp", 800, 190, "[(780,180), (820,200)]")
        ]
    }

    for gym, sector_list in sectors.items():
        cursor.execute("SELECT id FROM gyms WHERE name = ?;", (gym,))
        gym_id = cursor.fetchone()[0]
        cursor.executemany("""
            INSERT INTO sectors (name, gym_id, center_x, center_y, boundary_points) 
            VALUES (?, ?, ?, ?, ?) ON CONFLICT(name, gym_id) DO NOTHING;
        """, [(s[0], gym_id, s[1], s[2], s[3]) for s in sector_list])

    for gym, sector_list in sectors.items():
        cursor.execute("SELECT id FROM gyms WHERE name = ?;", (gym,))
        gym_id = cursor.fetchone()[0]
        cursor.executemany("""
            INSERT INTO sectors (name, gym_id, center_x, center_y, boundary_points) 
            VALUES (?, ?, ?, ?, ?) ON CONFLICT(name, gym_id) DO NOTHING;
        """, [(s[0], gym_id, s[1], s[2], s[3]) for s in sector_list])

    # Insert grading schemes
    grades = {
        "ClimbO": ["verde", "blu", "giallo", "arancione", "rosso", "viola"],
        "Apuano Appeso": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
        "Farm": ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    }
    for gym, grade_list in grades.items():
        cursor.execute("SELECT id FROM gyms WHERE name = ?;", (gym,))
        gym_id = cursor.fetchone()[0]
        cursor.executemany("INSERT INTO grades (grade, gym_id) VALUES (?, ?) ON CONFLICT(grade, gym_id) DO NOTHING;",
                           [(g, gym_id) for g in grade_list])

    # Insert climbs
    climbs = [
        ("ClimbO", "diedro", "rosso", "Jacopo", "verde", "2025-02-02"),
        ("Apuano Appeso", "Strapiombo", "4", "Leo", "rosa", "2025-02-17"),
        ("Farm", "fungo", "8", "Rugo", "nera", "2025-03-01")
    ]
    for gym, sector, grade, setter, hold_color, date in climbs:
        cursor.execute("SELECT id FROM gyms WHERE name = ?;", (gym,))
        gym_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM sectors WHERE name = ? AND gym_id = ?;", (sector, gym_id))
        sector_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM grades WHERE grade = ? AND gym_id = ?;", (grade, gym_id))
        grade_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM setters WHERE name = ?;", (setter,))
        setter_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO climbs (sector_id, gym_id, grade_id, setter_id, date_set, hold_color) 
            VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT DO NOTHING;
        """, (sector_id, gym_id, grade_id, setter_id, date, hold_color))

    conn.commit()
    conn.close()
    print("✅ Data inserted successfully!")

if __name__ == "__main__":
    insert_data()
