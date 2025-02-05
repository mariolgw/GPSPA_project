import psycopg2
import csv

# Database connection parameters
DB_PARAMS = {
    "dbname": "metro",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",  # Use the correct host, e.g., "127.0.0.1" or remote address
    "port": 5432          # Default PostgreSQL port
}

# File path for the CSV file
csv_file_path = "processed_file.csv"

# Connect to the database
try:
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()
    print("Connected to the database successfully.")
    
    # Open and read the CSV file
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        
        # Insert each row into the table
        for row in reader:
            cursor.execute("""
                INSERT INTO your_table_name (column1, column2, column3)
                VALUES (%s, %s, %s)
            """, row)
    
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
