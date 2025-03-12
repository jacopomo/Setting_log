from flask import Flask, render_template, request, redirect, jsonify, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('climbing_gym.db')
    conn.row_factory = sqlite3.Row  # Ensures results are returned as dictionaries
    return conn

@app.route('/')
def index():
    conn = get_db_connection()

    # Fetch gyms and setters for the dropdown
    gyms = conn.execute('SELECT id, name FROM gyms').fetchall()
    setters = conn.execute('SELECT id, name FROM setters').fetchall()

    # Fetch existing climbs from the database
    climbs = conn.execute('''
    SELECT climbs.id, climbs.color, grades.grade AS grade, climbs.date_set, 
           sectors.name AS sector_name, gyms.name AS gym_name, 
           setters.name AS setter_name
        FROM climbs
        JOIN sectors ON climbs.sector_id = sectors.id
        JOIN gyms ON sectors.gym_id = gyms.id
        JOIN setters ON climbs.setter_id = setters.id
        JOIN grades ON climbs.grade_id = grades.id
        ORDER BY climbs.date_set DESC;
    ''').fetchall()

    conn.close()

    return render_template('index.html', gyms=gyms, setters=setters, climbs=climbs)

@app.route('/get_sectors/<int:gym_id>', methods=['GET'])
def get_sectors(gym_id):
    conn = get_db_connection()
    
    # Fetch sectors based on the gym id
    sectors = conn.execute('''
        SELECT id, name FROM sectors WHERE gym_id = ?
    ''', (gym_id,)).fetchall()

    conn.close()

    # Format the sectors as a list of dictionaries for easier handling in JavaScript
    sectors_list = [{'id': sector['id'], 'name': sector['name']} for sector in sectors]
    
    # Return the sectors as JSON
    return jsonify({'sectors': sectors_list})

@app.route('/get_climbs/<int:sector_id>', methods=['GET'])
def get_climbs(sector_id):
    conn = get_db_connection()

    # Fetch climbs for the given sector
    climbs = conn.execute('''
        SELECT climbs.id, climbs.color, grades.grade AS grade, climbs.date_set, 
               setters.name AS setter
        FROM climbs
        JOIN grades ON climbs.grade_id = grades.id
        JOIN setters ON climbs.setter_id = setters.id
        WHERE climbs.sector_id = ?
        ORDER BY climbs.date_set DESC;
    ''', (sector_id,)).fetchall()

    conn.close()

    # Format the climbs as a list of dictionaries for easier handling in JavaScript
    climbs_list = [{'color': climb['color'], 'grade': climb['grade'], 'setter': climb['setter'], 'date': climb['date_set']} for climb in climbs]
    
    # Return the climbs as JSON
    return jsonify({'climbs': climbs_list})


@app.route('/get_gym_map/<int:gym_id>', methods=['GET'])
def get_gym_map(gym_id):
    try:
        conn = sqlite3.connect('climbing_gym.db')
        cursor = conn.cursor()

        # Query for the map path for the given gym_id
        cursor.execute("SELECT map_path FROM gyms WHERE id = ?", (gym_id,))
        result = cursor.fetchone()
        
        conn.close()

        if result:
            map_path = result[0]
            return jsonify({'map_url': map_path})
        else:
            return jsonify({'error': 'Gym not found'}), 404

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
