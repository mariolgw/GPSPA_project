from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime, time

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

@app.route('/t_n_e', methods=['GET'])
def t_n_e():
    """Get next 3 trains after current time for a given stop."""
    stop_id = request.args.get('stop_id')
    if not stop_id:
        return jsonify({"error": "stop_id parameter is required"}), 400

    # Get current time as TIME type
    current_time = datetime.now().time()
    
    # Get current weekday (A_WKDY_013 format from your data)
    weekday = 'A_WKDY_013'  # You might want to make this dynamic based on actual day
    
    conn = db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    query = sql.SQL("""
        SELECT 
            dt.stop_id,
            dt.departure_time,
            dt.stop_headsign,
            s.stop_name,
            si.route_short_name
        FROM departure_times dt
        JOIN stops s ON dt.stop_id = s.stop_id
        LEFT JOIN station_info si ON dt.stop_id = si.stop_id
        WHERE 
            dt.stop_id = %s
            AND dt.weekday = %s
            AND dt.departure_time > %s
        ORDER BY dt.departure_time
        LIMIT 3
    """)
    
    cur.execute(query, (stop_id, weekday, current_time))
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