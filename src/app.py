from flask import Flask, render_template, request, jsonify
import sqlite3
from pathlib import Path

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('eu_kontroll.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    # Get top 20 most reliable vehicles
    top_vehicles = conn.execute('''
        SELECT *
        FROM vehicle_stats
        ORDER BY approval_rate DESC, avg_serious_faults ASC
        LIMIT 20
    ''').fetchall()
    
    # Get bottom 20 least reliable vehicles
    bottom_vehicles = conn.execute('''
        SELECT *
        FROM vehicle_stats
        ORDER BY approval_rate ASC, avg_serious_faults DESC
        LIMIT 20
    ''').fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         top_vehicles=top_vehicles,
                         bottom_vehicles=bottom_vehicles)

@app.route('/search')
def search():
    query = request.args.get('query', '').upper()
    conn = get_db_connection()
    
    results = conn.execute('''
        SELECT *
        FROM vehicle_stats
        WHERE UPPER(make) LIKE ? OR UPPER(model) LIKE ?
        ORDER BY approval_rate DESC
    ''', (f'%{query}%', f'%{query}%')).fetchall()
    
    conn.close()
    return jsonify([dict(row) for row in results])

if __name__ == '__main__':
    app.run(debug=True)
