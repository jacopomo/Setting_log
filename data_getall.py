import sqlite3

DB_FILENAME = "climbing_gym.db"

def get_all_gyms():
    """Fetch all gyms from the database."""
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gyms")
    gyms = cursor.fetchall()
    conn.close()
    return gyms

def get_sectors_in_gym(gym_id):
    """Fetch all sectors belonging to a specific gym."""
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sectors WHERE gym_id = ?", (gym_id,))
    sectors = cursor.fetchall()
    conn.close()
    return sectors

def get_grades_for_gym(gym_id):
    """Fetch the grading scheme for a specific gym."""
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, grade FROM grades WHERE gym_id = ?", (gym_id,))
    grades = cursor.fetchall()
    conn.close()
    return grades

def get_climbs_in_sector(sector_id):
    """Fetch all climbs in a sector, displaying the correct grade from the grades table."""
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT climbs.id, sectors.name, setters.name, climbs.color, grades.grade, climbs.date_set 
        FROM climbs
        JOIN sectors ON climbs.sector_id = sectors.id
        JOIN setters ON climbs.setter_id = setters.id
        JOIN grades ON climbs.grade_id = grades.id
        WHERE climbs.sector_id = ?
    """, (sector_id,))
    climbs = cursor.fetchall()
    conn.close()
    return climbs

def get_climbs_by_setter(setter_id):
    """Fetch all climbs by a specific setter, including sector and grade information."""
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT climbs.id, sectors.name, setters.name, climbs.color, grades.grade, climbs.date_set 
        FROM climbs
        JOIN sectors ON climbs.sector_id = sectors.id
        JOIN setters ON climbs.setter_id = setters.id
        JOIN grades ON climbs.grade_id = grades.id
        WHERE climbs.setter_id = ?
    """, (setter_id,))
    climbs = cursor.fetchall()
    conn.close()
    return climbs

# Testing the functions
if __name__ == "__main__":
    print("All Gyms:", get_all_gyms())
    print("Sectors in Gym 1:", get_sectors_in_gym(1))
    print("Grades for Gym 1:", get_grades_for_gym(1))
    print("Climbs in Sector 1:", get_climbs_in_sector(1))
    print("Climbs by Setter 1:", get_climbs_by_setter(1))
