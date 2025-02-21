from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime

app = Flask(__name__)

def db_connection():
    """Establish a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        dbname="metro",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    return conn

@app.route('/tne', methods=['GET'])
def tne():
    """Get next 3 trains after current time."""
    stop_id = request.args.get('stop_id')
    if not stop_id:
        return jsonify({"error": "stop_id parameter is required"}), 400

    # Get current time as a time object (without date)
    current_time = datetime.now().time()
    
    conn = db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Simple query comparing times
    query = sql.SQL("""
        SELECT 
            stop_id, 
            stop_headsign, 
            departure_time
        FROM departure_times 
        WHERE 
            stop_id = %s 
            AND departure_time > %s
        ORDER BY departure_time 
        LIMIT 3
    """)
    
    cur.execute(query, (stop_id, current_time))
    trains = cur.fetchall()

    # Format departure times as strings
    for train in trains:
        train['departure_time'] = train['departure_time'].strftime('%H:%M:%S')

    # Close database connection
    cur.close()
    conn.close()

    if trains:
        return jsonify({"trains": trains})
    return jsonify({"error": "No upcoming trains found"}), 404

if __name__ == '__main__':
    app.run(debug=True)