from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
#from utils import format_geojson


app = Flask(__name__)

def db_connection():
    """Establish a connection to the PostgreSQL database."""
    # connect to the postgres DB. values may change depending on your postgres setup
    conn = psycopg2.connect(
        dbname="metro",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )

    return conn

#get station info
@app.route('/station_info', methods=['GET'])
def get_station_info():
    """Retrieve station information from the database."""
    stop_id = request.args.get('stop_id')
    if not stop_id:
        return jsonify({"error": "stop_id parameter is required"}), 400

    conn = db_connection()
    
    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a query
    query = sql.SQL("SELECT stop_name, stop_lat, stop_lon FROM stops WHERE stop_id = %s")
    cur.execute(query, (stop_id,))

    # Retrieve query results
    station = cur.fetchone()

    if station:
        response = jsonify(station)
    else:
        response = jsonify({"error": "Station not found"}), 404

    # Close communication with the database
    cur.close()
    conn.close()

    return response

@app.route('/next_trains', methods=['GET'])
def get_next_trains():
    """Retrieve the next 3 trains for a given station."""
    stop_id = request.args.get('stop_id')
    if not stop_id:
        return jsonify({"error": "stop_id parameter is required"}), 400

    conn = db_connection()
    
    # Open a cursor to perform database operations
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Execute a query to get the next 3 trains
    query = sql.SQL("""
        SELECT stop_id, stop_headsign, departure_time 
        FROM departure_times 
        WHERE stop_id = %s 
        ORDER BY departure_time 
        LIMIT 3
    """)
    cur.execute(query, (stop_id,))

    # Retrieve query results
    trains = cur.fetchall()
    
    # Convert departure_time to string format
    for train in trains:
        train['departure_time'] = train['departure_time'].strftime('%H:%M:%S')

    if trains:
        response = jsonify(trains)
    else:
        response = jsonify({"error": "No upcoming trains found"}), 404

    # Close communication with the database
    cur.close()
    conn.close()

    return response

@app.route('/refresh', methods=['POST'])
def refresh_page():
    """Refresh the page."""
    return jsonify({"message": "Page refreshed"}), 200
        


if __name__ == '__main__':
    app.run(debug=True)

