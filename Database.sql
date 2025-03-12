-- Create the gyms table
CREATE TABLE IF NOT EXISTS gyms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    map_path TEXT NOT NULL
);

-- Create the grading schemes table (simplified structure)
CREATE TABLE IF NOT EXISTS grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique grade id
    gym_id INTEGER NOT NULL,               -- Gym reference
    grade TEXT NOT NULL,                   -- Grade name (e.g., Verde, Blu, etc.)
    FOREIGN KEY (gym_id) REFERENCES gyms(id) ON DELETE CASCADE
);

CREATE TABLE sectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gym_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    x INTEGER NOT NULL,
    y INTEGER NOT NULL,
    FOREIGN KEY (gym_id) REFERENCES gyms(id)
);



-- Create the setters table
CREATE TABLE IF NOT EXISTS setters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE climbs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gym_id INTEGER NOT NULL,
    sector_id INTEGER NOT NULL,
    setter_id INTEGER NOT NULL,
    color TEXT NOT NULL,
    grade_id INTEGER NOT NULL,
    date_set TEXT NOT NULL,
    FOREIGN KEY (gym_id) REFERENCES gyms(id),
    FOREIGN KEY (sector_id) REFERENCES sectors(id),
    FOREIGN KEY (setter_id) REFERENCES setters(id),
    FOREIGN KEY (grade_id) REFERENCES grades(id)
);


-- Create the climb_archive table (Stores removed climbs)
CREATE TABLE IF NOT EXISTS climb_archive (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gym_id INTEGER NOT NULL,
    climb_id INTEGER NOT NULL,
    sector_id INTEGER NOT NULL,
    setter_id INTEGER NOT NULL,
    color TEXT NOT NULL,
    grade_id INTEGER NOT NULL,
    date_set DATE NOT NULL,
    date_removed DATE NOT NULL,
    FOREIGN KEY (gym_id) REFERENCES gyms(id) ON DELETE CASCADE,
    FOREIGN KEY (climb_id) REFERENCES climbs(id) ON DELETE CASCADE,
    FOREIGN KEY (sector_id) REFERENCES sectors(id) ON DELETE CASCADE,
    FOREIGN KEY (setter_id) REFERENCES setters(id) ON DELETE CASCADE,
    FOREIGN KEY (grade_id) REFERENCES grades(id) ON DELETE CASCADE
);