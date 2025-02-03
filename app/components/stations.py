import pandas as pd
import json

class StationListGenerator:
    def __init__(self, db_path):
        """
        Initialize with database connection details
        :param db_path: Path to your SQLite database file
        """
        self.db_path = db_path
    
    def get_stations_postgres(self):
        """
        Get stations from PostgreSQL database
        """
        try:
            conn = psycopg2.connect(
                dbname="your_db_name",
                user="your_username",
                password="your_password",
                host="your_host"
            )
            
            query = """
            SELECT stop_id, stop_name
            FROM stops
            WHERE location_type = 1
            OR location_type IS NULL
            ORDER BY stop_name;
            """
            
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            return df
            
        except Exception as e:
            print(f"Error fetching stations: {e}")
            return pd.DataFrame()

def main():
    # Example usage
    db_path = 'path/to/your/gtfs.db'  # Replace with your database path
    generator = StationListGenerator(db_path)
    
    # Get stations from database
    stations = generator.get_stations_sqlite()
    
    # Generate and save HTML
    if not stations.empty:
        html_content = generator.generate_html(stations)
        generator.save_html(html_content)

if __name__ == "__main__":
    main()