import sqlite3
from datetime import date

DB_FILENAME = "climbing_gym.db"
def get_all_gyms():
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gyms")
    gyms = cursor.fetchall()
    conn.close()
    return gyms

# Print all gyms
print(get_all_gyms())

def get_sectors_in_gym(gym_id):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sectors WHERE gym_id = ?", (gym_id,))
    sectors = cursor.fetchall()
    conn.close()
    return sectors

# Print all sectors for gym ID 1 (Rocky Peaks Gym)
print(get_sectors_in_gym(1))

def get_climbs_in_sector(sector_id):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM climbs WHERE sector_id = ?", (sector_id,))
    climbs = cursor.fetchall()
    conn.close()
    return climbs

# Print all climbs for sector ID 1
print(get_climbs_in_sector(1))

def get_climbs_by_setter(setter_id):
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM climbs WHERE setter_id = ?", (setter_id,))
    climbs = cursor.fetchall()
    conn.close()
    return climbs


if __name__ == "__main__":
    print(get_all_gyms())
    print(get_sectors_in_gym(1))
    print(get_climbs_in_sector(1))
    print(get_climbs_by_setter(1))


