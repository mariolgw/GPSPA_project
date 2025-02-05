import os
import requests
import zipfile
import datetime
from pathlib import Path
import schedule
import time

# URL of the GTFS data
GTFS_URL = "https://www.metrolisboa.pt/google_transit/googleTransit.zip"

# Destination folder
ETL_DIR = Path(os.path.dirname(__file__)).parent / "ETL" / "data"  # Assuming ETL/data directory is at the same level as API directory
print(ETL_DIR)
ZIP_FILE = ETL_DIR / "googleTransit.zip"


# Create the directory if it doesn't exist
ETL_DIR.mkdir(parents=True, exist_ok=True)

def download_and_unzip():
    """Downloads and unzips the GTFS data"""
    print(f"[{datetime.datetime.now()}] Downloading GTFS data...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Authorization': 'Bearer AMf-vBxBvVKDdIToXLEthMXkFVFejxG04g7Ei6S2WThFRLnmWIxzOKxEvl-zRh08BD-yBJwZT-CfGR2SBLe-qcFvxR20t8l7nLaw5a1c-icB5NplCQMdyrCLaFBNItj1JF_3AJyKUYtudsODhRV5AQOLJU92aUH330XVZFQ9OMo3fRBCcW3TQpU-4zjysTUkkM7JeKYiUyA4pTtMZ3N6Gkmintr1iDvvkpU2zWLXJlPIS0QgRJzn_oSjGG3EKWAhQKcEtXm0tMWp6rKW0m0EdtLM0EW4j5qjTHWPoanUOSnracLdt8OOB6TMdDOg7xGYxC6F-bb1ekf0TC-icTlQ00AEm1QdxeEHYZzx0b7I8u_Ek2k0qe7QAVE'
    }

    # Download the file
    response = requests.get(GTFS_URL, headers=headers, stream=True)
    print(response.status_code)
    if response.status_code == 200:
        with open(ZIP_FILE, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print("Download complete!")

        # Unzip the file
        print("Unzipping...")
        with zipfile.ZipFile(ZIP_FILE, "r") as zip_ref:
            zip_ref.extractall(ETL_DIR)
        print(f"Files extracted to {ETL_DIR}")

        # Optionally, delete the zip file after extraction
        os.remove(ZIP_FILE)
        print("Zip file removed.")
    else:
        print("Failed to download file. Check the URL.")

# Schedule the script to run every Monday and Thursday
schedule.every().monday.at("06:00").do(download_and_unzip)  # Runs at 08:00 AM
schedule.every().thursday.at("06:00").do(download_and_unzip)

print("Scheduler running... (Press Ctrl+C to stop)")

download_and_unzip()


def get_next_run_time():
    """Returns the time in seconds until the next scheduled run"""
    next_run = min(schedule.next_run().timestamp(), schedule.next_run().timestamp())
    return max(0, next_run - time.time())

# Keep the script running and sleep until the next scheduled task
while True:
    schedule.run_pending()
    sleep_time = get_next_run_time()
    print(f"Sleeping for {sleep_time} seconds...")
    time.sleep(sleep_time)
