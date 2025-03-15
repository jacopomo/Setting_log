from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('climbing_gym.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()

    gyms = conn.execute("SELECT id, name FROM gyms").fetchall()
    setters = conn.execute("SELECT id, name FROM setters").fetchall()
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

@app.route('/get_sectors/<gym_name>', methods=['GET'])
def get_sectors(gym_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM gyms WHERE name = ?", (gym_name,))
    gym = cursor.fetchone()
    if not gym:
        return jsonify({'error': 'Gym not found'}), 404

    gym_id = gym[0]
    cursor.execute("SELECT id, name, center_x, center_y, boundary_points FROM sectors WHERE gym_id = ?", (gym_id,))
    sectors = cursor.fetchall()
    
    conn.close()

    return jsonify({'sectors': [{'id': s[0], 'name': s[1], 'center_x': s[2], 'center_y': s[3], 'boundary_points': s[4]} for s in sectors]})

@app.route('/get_gym_map/<gym_name>', methods=['GET'])
def get_gym_map(gym_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT map_location FROM gyms WHERE name = ?", (gym_name,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0]:
        return jsonify({'map_url': result[0]})
    
    return jsonify({'error': 'Gym not found'}), 404

@app.route('/get_grades/<gym_name>', methods=['GET'])
def get_grades(gym_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM gyms WHERE name = ?", (gym_name,))
    gym = cursor.fetchone()
    if not gym:
        return jsonify({'error': 'Gym not found'}), 404
    
    gym_id = gym[0]
    cursor.execute("SELECT grade FROM grades WHERE gym_id = ?", (gym_id,))
    grades = cursor.fetchall()

    conn.close()
    
    return jsonify({'grades': [{'grade': g[0]} for g in grades]})

@app.route('/get_climbs/<int:sector_id>', methods=['GET'])
def get_climbs(sector_id):
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

    return jsonify({'climbs': [{'color': c['hold_color'], 'grade': c['grade'], 
                                'setter': c['setter'], 'date': c['date_set']} 
                               for c in climbs]})

@app.route('/get_climbs_by_gym/<gym_name>', methods=['GET'])
def get_climbs_by_gym(gym_name):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get the gym ID
    cursor.execute("SELECT id FROM gyms WHERE name = ?", (gym_name,))
    gym = cursor.fetchone()
    if not gym:
        return jsonify({'error': 'Gym not found'}), 404
    
    gym_id = gym[0]

    # Fetch climbs for this gym
    cursor.execute("""
        SELECT climbs.id, climbs.hold_color, grades.grade, climbs.date_set, 
               sectors.name AS sector_name, gyms.name AS gym_name, 
               setters.name AS setter_name
        FROM climbs
        JOIN sectors ON climbs.sector_id = sectors.id
        JOIN gyms ON climbs.gym_id = gyms.id
        JOIN setters ON climbs.setter_id = setters.id
        JOIN grades ON climbs.grade_id = grades.id
        WHERE climbs.gym_id = ?
        ORDER BY climbs.date_set DESC;
    """, (gym_id,))
    climbs = cursor.fetchall()

    conn.close()

    return jsonify({'climbs': [
        {'id': c[0], 'hold_color': c[1], 'grade': c[2], 'date_set': c[3],
         'sector_name': c[4], 'gym_name': c[5], 'setter_name': c[6]}
        for c in climbs
    ]})



# ✅ Route to insert a new climb
@app.route('/add_climb', methods=['POST'])
def add_climb():
    data = request.json

    if not data or not all(k in data for k in ["gym", "sector", "grade", "setter", "color", "date"]):
        return jsonify({"error": "Missing required fields"}), 400  # ✅ Proper error handling

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
    # Get necessary IDs from database
        cursor.execute("SELECT id FROM gyms WHERE name = ?", (data['gym'],))
        gym = cursor.fetchone()
        if not gym:
            return jsonify({"error": "Gym not found"}), 404
        gym_id = gym[0]
    
        cursor.execute("SELECT id FROM sectors WHERE name = ? AND gym_id = ?", (data['sector'], gym_id))
        sector = cursor.fetchone()
        if not sector:
            return jsonify({"error": "Sector not found"}), 404
        sector_id = sector[0]

        cursor.execute("SELECT id FROM grades WHERE grade = ? AND gym_id = ?", (data['grade'], gym_id))
        grade = cursor.fetchone()
        if not grade:
            return jsonify({"error": "Grade not found"}), 404
        grade_id = grade[0]

        cursor.execute("SELECT id FROM setters WHERE name = ?", (data['setter'],))
        setter = cursor.fetchone()
        if not setter:
            return jsonify({"error": "Setter not found"}), 404
        setter_id = setter[0]

        # Insert new climb
        cursor.execute("""
            INSERT INTO climbs (sector_id, gym_id, grade_id, setter_id, date_set, hold_color) 
            VALUES (?, ?, ?, ?, ?, ?);
        """, (sector_id, gym_id, grade_id, setter_id, data['date'], data['color']))

        conn.commit()
        return jsonify({"message": "Climb added successfully!"}), 201
        
    except Exception as e:
            return jsonify({"error": str(e)}), 500  # ✅ Catch and return errors

    finally:
        conn.close()

# ✅ Route to delete a climb
@app.route('/delete_climb/<int:climb_id>', methods=['DELETE'])
def delete_climb(climb_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM climbs WHERE id = ?", (climb_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Climb deleted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)