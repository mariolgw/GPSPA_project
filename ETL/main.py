import sys
import os
import requests
import pandas
import psycopg2
import json
import schedule

# Add the parent directory of ETL to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
print("Python path:", sys.path)

from scripts.importrequests import download_and_unzip  # Import the function
from scripts.processing_data import process_data
from scripts.timeconverte import process_times
from scripts.dbconnection import main as db_main, DB_PARAMS, stops_file_path, arrival_times_file_path, station_info_file_path
from scripts.dbconnection import insert_stops, insert_departure_times, insert_station_info

def main():
    
    # Step 1: Download and unzip the file
    download_and_unzip()
    
    # Step 2: Process the data
    processed_data_file = process_data('ETL/data/stop_times.txt')  # Adjust the path as needed
    
    # Step 3: Convert the time

    input_file = processed_data_file
    output_file = 'ETL/data/stop_times_output.txt'
    process_times(input_file, output_file)
    
    # Step 4: Insert into the database
    db_main()

    conn = psycopg2.connect(**DB_PARAMS) #declaring vaiable to connect to the database
    cursor = conn.cursor()

    insert_stops(cursor, stops_file_path)
    insert_departure_times(cursor, arrival_times_file_path)
    insert_station_info(cursor, station_info_file_path)

if __name__ == "__main__":
    main()
    