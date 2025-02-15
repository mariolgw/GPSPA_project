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

if __name__ == '__main__':
    app.run(debug=True)

