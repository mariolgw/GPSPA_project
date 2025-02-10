import psycopg2
import csv
import json

# Database connection parameters
DB_PARAMS = {
    "dbname": "metro",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",  # Use the correct host, e.g., "127.0.0.1" or remote address
    "port": 5432          # Default PostgreSQL port
}

# File paths for the input files
stops_file_path = "data/stops.txt"
arrival_times_file_path = "data/grouped_result_fixed.txt"
station_info_file_path = "data/station_info (1).json"

# Connect to the database
try:
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    print("Connected to the database successfully.")
    
    # Truncate the tables to remove old data
    cursor.execute("TRUNCATE TABLE departure_times, station_info, stops RESTART IDENTITY CASCADE")
    print("Old data removed successfully.")
    
    # Insert data into stops table
    with open(stops_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        for row in reader:
            stop_id, _, _, stop_lat, stop_lon, _, _, _, _ = row
            cursor.execute("""
                INSERT INTO stops (stop_id, stop_lat, stop_lon)
                VALUES (%s, %s, %s)
            """, (stop_id, stop_lat, stop_lon))
    
    # Insert data into departure_times table
    with open(arrival_times_file_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)  # Skip the header row
        
        for row in reader:
            weekday, stop_id, departure_time, stop_headsign = row
            cursor.execute("""
                INSERT INTO departure_times (weekday, stop_id, departure_time, stop_headsign)
                VALUES (%s, %s, %s, %s)
            """, (weekday, stop_id, departure_time, stop_headsign))
    
    # Insert data into station_info table
    with open(station_info_file_path, 'r') as file:
        data = json.load(file)
        
        for station, infos in data.items():
            for info in infos:
                stop_id = info.get("stop_id")
                trip_id = info.get("trip_id")
                stop_url = info.get("stop_url")
                stop_headsign = info.get("stop_headsign")
                route_short_name = info.get("route_short_name")
                route_long_name = info.get("route_long_name")
                route_color = info.get("route_color")
                
                cursor.execute("""
                    INSERT INTO station_info (stop_id, trip_id, stop_url, stop_headsign, route_short_name, route_long_name, route_color)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (stop_id, trip_id, stop_url, stop_headsign, route_short_name, route_long_name, route_color))
    
    # Commit changes and close the connection
    conn.commit()
    print("Data added successfully!")
except Exception as e:
    print("Error:", e)
finally:
    if conn:
        cursor.close()
        conn.close()
        print("Database connection closed.")