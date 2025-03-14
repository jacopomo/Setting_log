-- Create the gyms table
CREATE TABLE gyms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    map_location TEXT -- Stores the file path to the gym's layout map
);

-- Create the sectors table (each sector belongs to a gym)
CREATE TABLE sectors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gym_id INTEGER NOT NULL,
    center_x INTEGER,
    center_y INTEGER,
    boundary_points TEXT,
    FOREIGN KEY (gym_id) REFERENCES gyms(id) ON DELETE CASCADE,
    UNIQUE (name, gym_id) -- Ensures sector names are unique within a gym
);

-- Create the setters table (people who set climbs)
CREATE TABLE setters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

-- Create the grades table (each gym has its own grading system)
CREATE TABLE grades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grade TEXT NOT NULL,
    gym_id INTEGER NOT NULL,
    FOREIGN KEY (gym_id) REFERENCES gyms(id) ON DELETE CASCADE,
    UNIQUE (grade, gym_id) -- Ensures grade uniqueness per gym
);

-- Create the climbs table (each climb belongs to a sector and follows a gym's grading system)
CREATE TABLE climbs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_id INTEGER NOT NULL,
    gym_id INTEGER NOT NULL,
    grade_id INTEGER NOT NULL,
    setter_id INTEGER NOT NULL,
    date_set DATE NOT NULL,
    hold_color TEXT NOT NULL,
    FOREIGN KEY (sector_id) REFERENCES sectors(id) ON DELETE CASCADE,
    FOREIGN KEY (gym_id) REFERENCES gyms(id) ON DELETE CASCADE,
    FOREIGN KEY (grade_id) REFERENCES grades(id) ON DELETE CASCADE,
    FOREIGN KEY (setter_id) REFERENCES setters(id) ON DELETE SET NULL
);