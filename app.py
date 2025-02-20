from flask import Flask, render_template, request, redirect, jsonify
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
    SELECT climbs.id, climbs.color, climbs.grade, climbs.date_set, 
           sectors.name AS sector_name, gyms.name AS gym_name, 
           setters.name AS setter_name
        FROM climbs
        JOIN sectors ON climbs.sector_id = sectors.id
        JOIN gyms ON sectors.gym_id = gyms.id
        JOIN setters ON climbs.setter_id = setters.id
        ORDER BY climbs.date_set DESC;
    ''').fetchall()

    conn.close()

    return render_template('index.html', gyms=gyms, setters=setters, climbs=climbs)

@app.route('/add_climb', methods=['POST'])
def add_climb():
    # Get data from the form
    gym_id = request.form['gym']
    sector_id = request.form['sector']
    setter_id = request.form['setter']
    color = request.form['color']
    grade = request.form['grade']
    date_set = request.form['date_set']

    # Connect to the database and insert the new climb
    conn = get_db_connection()
    conn.execute('''
    INSERT INTO climbs (sector_id, setter_id, color, grade, date_set) 
    VALUES (?, ?, ?, ?, ?)
    ''', (sector_id, setter_id, color, grade, date_set))
    conn.commit()
    conn.close()

    # Redirect to the homepage to show the updated table
    return redirect('/')

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

if __name__ == '__main__':
    app.run(debug=True)
