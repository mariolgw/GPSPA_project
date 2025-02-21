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
    Parameters: stop_id
    """
    stop_id = request.args.get('stop_id')
    if not stop_id:
        return jsonify({"error": "stop_id parameter is required"}), 400

    conn = db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Modified query to only return routes that have scheduled trains
    query = sql.SQL("""
        SELECT DISTINCT
            s.stop_id,
            s.stop_name,
            s.stop_lat,
            s.stop_lon,
            si.route_short_name,
            si.route_long_name,
            si.route_color
        FROM stops s
        JOIN station_info si ON s.stop_id = si.stop_id
        WHERE s.stop_id = %s
        AND EXISTS (
            SELECT 1 
            FROM departure_times dt 
            WHERE dt.stop_id = s.stop_id 
            AND dt.stop_id = si.stop_id
            AND dt.departure_time > CURRENT_TIME
        )
    """)
    
    cur.execute(query, (stop_id,))
    station = cur.fetchall()
    
    cur.close()
    conn.close()

    if station:
        return jsonify(station)
    return jsonify({"error": "Station not found"}), 404

@app.route('/next_trains', methods=['GET'])
def next_trains():
    """
    Get next 3 trains per direction after current time, accounting for weekday/weekend schedules.
    """
    stop_id = request.args.get('stop_id')
    if not stop_id:
        return jsonify({"error": "stop_id parameter is required"}), 400
    
    current_time = datetime.now().time()
    current_weekday = datetime.now().weekday()
    is_weekday = 1 if current_weekday < 5 else 0
    
    conn = db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Modified query to get next 3 trains per direction
    query = sql.SQL("""
        WITH DirectionalTrains AS (
            SELECT 
                dt.stop_id, 
                dt.stop_headsign, 
                dt.departure_time,
                si.route_short_name,
                si.route_long_name,
                ROW_NUMBER() OVER (
                    PARTITION BY dt.stop_headsign 
                    ORDER BY dt.departure_time
                ) as rn
            FROM departure_times dt
            LEFT JOIN station_info si ON dt.stop_id = si.stop_id
            WHERE 
                dt.stop_id = %s 
                AND dt.departure_time > %s
                AND dt.weekday = %s::text
                AND si.route_short_name IS NOT NULL  -- Filter out empty routes
        )
        SELECT *
        FROM DirectionalTrains
        WHERE rn <= 3
        ORDER BY stop_headsign, departure_time
    """)
    
    cur.execute(query, (stop_id, current_time, is_weekday))
    trains = cur.fetchall()

    # Group trains by direction
    directions = {}
    for train in trains:
        direction = train['stop_headsign']
        if direction not in directions:
            directions[direction] = []
            
        train_dict = dict(train)
        train_dict['departure_time'] = train_dict['departure_time'].strftime('%H:%M:%S')
        # Calculate countdown
        departure_time = datetime.strptime(train_dict['departure_time'], '%H:%M:%S').time()
        current_datetime = datetime.now()
        departure_datetime = datetime.combine(current_datetime.date(), departure_time)
        
        # Handle cases where train is after midnight
        if departure_time < current_time:
            departure_datetime += timedelta(days=1)
            
        time_diff = departure_datetime - current_datetime
        minutes = int(time_diff.total_seconds() / 60)
        hours = minutes // 60
        remaining_minutes = minutes % 60
        
        if hours > 0:
            train_dict['countdown'] = f"{hours}h {remaining_minutes}m"
        else:
            train_dict['countdown'] = f"{remaining_minutes}m"
            
        directions[direction].append(train_dict)

    cur.close()
    conn.close()

    if directions:
        return jsonify({"directions": directions})
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