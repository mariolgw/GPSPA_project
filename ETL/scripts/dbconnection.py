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
arrival_times_file_path = "ETL/data/stop_times_output.txt"
station_info_file_path = "data/station_info (1).json"

def insert_stops(cursor, file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        for row in reader:
            stop_id, stop_name, _, stop_lat, stop_lon, _, _, _, _ = row
            cursor.execute("""
                INSERT INTO stops (stop_id,stop_name, stop_lat, stop_lon)
                VALUES (%s,%s, %s, %s)
            """, (stop_id,stop_name, stop_lat, stop_lon))
            # Debugging comment: Check if the row is being processed correctly
            print(f"Inserted stop: {stop_id},{stop_name} {stop_lat}, {stop_lon}")

def insert_departure_times(cursor, file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        for row in reader:
            weekday, stop_id, departure_time, stop_headsign = row
            cursor.execute("""
                INSERT INTO departure_times (weekday, departure_time ,stop_id ,stop_headsign)
                VALUES (%s, %s, %s, %s)
            """, (weekday, stop_id, departure_time, stop_headsign))
            # Debugging comment: Check if the row is being processed correctly
            print(f"Inserted departure time: {weekday}, {stop_id}, {departure_time}, {stop_headsign}")

def insert_station_info(cursor, file_path):
    with open(file_path, 'r') as file:
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
                # Debugging comment: Check if the row is being processed correctly
                print(f"Inserted station info: {stop_id}, {trip_id}, {stop_url}, {stop_headsign}, {route_short_name}, {route_long_name}, {route_color}")

def main():
    # Connect to the database
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    print("Connected to the database successfully.")

    # Truncate the tables to remove old data
    cursor.execute("TRUNCATE TABLE departure_times, station_info, stops RESTART IDENTITY CASCADE")
    print("Old data removed successfully.")

    # Insert data into tables
    insert_stops(cursor, stops_file_path)
    insert_departure_times(cursor, arrival_times_file_path)
    insert_station_info(cursor, station_info_file_path)

    # Commit changes and close the connection
    conn.commit()
    print("Data added successfully!")

    if conn:
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()