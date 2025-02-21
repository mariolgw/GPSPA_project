from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def db_connection():
    """
    Establish a connection to the PostgreSQL database.

    Returns:
        conn (psycopg2.extensions.connection): Database connection object.
    """
    conn = psycopg2.connect(
        dbname="metro",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )
    return conn

@app.route('/station_info', methods=['GET'])
def get_station_info():
    """
    Retrieve station information from the database.

    Query Parameters:
        stop_id (str): The ID of the stop to retrieve information for.

    Returns:
        JSON response containing station information or an error message.
    """
    stop_id = request.args.get('stop_id')
    if not stop_id:
        return jsonify({"error": "stop_id parameter is required"}), 400

    conn = db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # SQL query to retrieve station information
    query = sql.SQL("""
        SELECT 
            s.stop_id,
            s.stop_name,
            s.stop_lat,
            s.stop_lon,
            si.route_short_name,
            si.route_long_name,
            si.route_color
        FROM stops s
        LEFT JOIN station_info si ON s.stop_id = si.stop_id
        WHERE s.stop_id = %s
    """)
    
    cur.execute(query, (stop_id,))
    station = cur.fetchone()
    
    cur.close()
    conn.close()

    if station:
        return jsonify(station)
    return jsonify({"error": "Station not found"}), 404

@app.route('/next_trains', methods=['GET'])
def next_trains():
    """
    Get next 3 trains after current time, accounting for weekday/weekend schedules.

    Query Parameters:
        stop_id (str): The ID of the stop to retrieve train information for.

    Returns:
        JSON response containing the next 3 trains or an error message.
    """
    stop_id = request.args.get('stop_id')
    if not stop_id:
        return jsonify({"error": "stop_id parameter is required"}), 400
    
    # Get current time 
    current_time = datetime.now().time()
    # Get current weekday (0-6, where 0 is Monday)
    current_weekday = datetime.now().weekday()
    # 1 for weekdays (0-4), 0 for weekends (5-6)
    is_weekday = 1 if current_weekday < 5 else 0
    
    conn = db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # SQL query to retrieve next 3 trains
    query = sql.SQL("""
        SELECT 
            dt.stop_id, 
            dt.stop_headsign, 
            dt.departure_time,
            si.route_short_name,
            si.route_long_name
        FROM departure_times dt
        LEFT JOIN station_info si ON dt.stop_id = si.stop_id
        WHERE 
            dt.stop_id = %s 
            AND dt.departure_time > %s
            AND dt.weekday = %s::text
        ORDER BY dt.departure_time 
        LIMIT 3
    """)
    
    cur.execute(query, (stop_id, current_time, is_weekday))
    trains = cur.fetchall()

    # Convert trains from RealDictRow to dict and format times
    formatted_trains = []
    for train in trains:
        train_dict = dict(train)
        train_dict['departure_time'] = train_dict['departure_time'].strftime('%H:%M:%S')
        formatted_trains.append(train_dict)

    cur.close()
    conn.close()

    if formatted_trains:
        return jsonify({"trains": formatted_trains})
    return jsonify({"error": "No upcoming trains found"}), 404

@app.route('/station_names', methods=['GET'])
def get_station_names():
    """
    Retrieve all unique station names and IDs for dropdown menu.

    Returns:
        JSON response containing a list of station names and IDs.
    """
    conn = db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # SQL query to retrieve unique station names and IDs
    query = sql.SQL("""
        SELECT DISTINCT stop_id, stop_name
        FROM stops
        ORDER BY stop_name
    """)
    
    cur.execute(query)
    stations = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # Return the raw data directly
    return jsonify(stations)

if __name__ == '__main__':
    app.run(debug=True)