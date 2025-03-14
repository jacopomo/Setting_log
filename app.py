from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Function to establish a database connection
def get_db_connection():
    conn = sqlite3.connect('climbing_gym.db')
    conn.row_factory = sqlite3.Row  # Enables dictionary-like access to rows
    return conn

@app.route('/')
def index():
    """Render the main page with gyms and climbs."""
    conn = get_db_connection()

    # Fetch gyms and setters for dropdowns
    gyms = conn.execute("SELECT id, name FROM gyms").fetchall()
    setters = conn.execute("SELECT id, name FROM setters").fetchall()

    # Fetch all existing climbs with details
    climbs = conn.execute("""
        SELECT climbs.id, climbs.hold_color, grades.grade, climbs.date_set, 
               sectors.name AS sector_name, gyms.name AS gym_name, 
               setters.name AS setter_name
        FROM climbs
        JOIN sectors ON climbs.sector_id = sectors.id
        JOIN gyms ON climbs.gym_id = gyms.id
        JOIN setters ON climbs.setter_id = setters.id
        JOIN grades ON climbs.grade_id = grades.id
        ORDER BY climbs.date_set DESC;
    """).fetchall()

    conn.close()

    return render_template('index.html', gyms=gyms, setters=setters, climbs=climbs)

@app.route('/get_sectors/<int:gym_id>', methods=['GET'])
def get_sectors(gym_id):
    conn = get_db_connection()
    sectors = conn.execute('''
        SELECT id, name, center_x, center_y FROM sectors WHERE gym_id = ?
    ''', (gym_id,)).fetchall()
    conn.close()

    # Convert result to list of dictionaries
    sectors_list = [
        {"id": s["id"], "name": s["name"], "center_x": s["center_x"], "center_y": s["center_y"]}
        for s in sectors
    ]
    
    return jsonify({"sectors": sectors_list})


@app.route('/get_climbs/<int:sector_id>', methods=['GET'])
def get_climbs(sector_id):
    """Fetches all climbs in a given sector."""
    conn = get_db_connection()
    climbs = conn.execute("""
        SELECT climbs.id, climbs.hold_color, grades.grade, climbs.date_set, 
               setters.name AS setter
        FROM climbs
        JOIN grades ON climbs.grade_id = grades.id
        JOIN setters ON climbs.setter_id = setters.id
        WHERE climbs.sector_id = ?
        ORDER BY climbs.date_set DESC;
    """, (sector_id,)).fetchall()
    conn.close()

    # Convert to JSON format
    return jsonify({'climbs': [{'color': c['hold_color'], 'grade': c['grade'], 
                                'setter': c['setter'], 'date': c['date_set']} 
                               for c in climbs]})

@app.route('/get_gym_map/<int:gym_id>', methods=['GET'])
def get_gym_map(gym_id):
    """Fetches the map location for a given gym."""
    conn = get_db_connection()
    result = conn.execute("SELECT map_location FROM gyms WHERE id = ?", (gym_id,)).fetchone()
    conn.close()

    if result:
        return jsonify({'map_url': result['map_location']})
    return jsonify({'error': 'Gym not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
