import psycopg2
from psycopg2 import sql

def get_station_info(stop_id):
    """Get information about a specific station from PostgreSQL database."""
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            dbname="metro",
            user="postgres",
            password="postgres",
            host="localhost",
            port=5432
        )

        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a query
        query = sql.SQL("SELECT stop_name, stop_lat, stop_lon FROM stops WHERE stop_id = %s")
        cur.execute(query, (stop_id,))

        # Retrieve query results
        station = cur.fetchone()

        if station:
            print(f"Stop Name: {station[0]}")
            print(f"Location: {station[1]}, {station[2]}")
        else:
            print("Station not found")

        # Close communication with the database
        cur.close()
        conn.close()

    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")

# Example usage
get_station_info('AM1')  # Replace with your actual stop_id