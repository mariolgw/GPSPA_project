import sys
import os
import requests
import pandas
#import flask
#import sqlalchemy
#import foliumgtfs-realtime-bindings
import psycopg2
import json
import schedule
import requests
import csv



from scripts.importrequests import download_and_unzip  # Import the function
from scripts.processing_data import process_data
from scripts.timeconverte import correct_time
from scripts.dbconnection import insert_stops, insert_departure_times, insert_station_info

def main():
    
    # Step 1: Download and unzip the file
    download_and_unzip()
    
    # Step 2: Process the data
    processed_data = process_data('data/stop_times.txt')  # Adjust the path as needed
    
    # Step 3: Convert the time
    converted_data = correct_time(processed_data)
    
    # Step 4: Insert into the database
    insert_stops(converted_data)
    insert_departure_times(converted_data)
    insert_station_info(converted_data)


if __name__ == "__main__":
    main()