import sys
import os
import requests
from processing_data import process_data
from timeconverte import correct_time
from dbconnection import insert_stops, insert_departure_times, insert_station_info

# Add the ETL/scripts directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ETL', 'scripts')))
from importrequests import download_and_unzip  # Import the function


def main():
    # Step 1: Get the zip file
    zip_url = 'http://example.com/data.zip'
    response = requests.get(zip_url)
    with open('data.zip', 'wb') as file:
        file.write(response.content)
    
    # Step 2: Process the data
    processed_data = process_data('data.zip')
    
    # Step 3: Convert the time
    converted_data = convert_time(processed_data)
    
    # Step 4: Insert into the database
    insert_into_db(converted_data)

if __name__ == "__main__":
    main()