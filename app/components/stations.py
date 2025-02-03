import psycopg2 
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
    def generate_html(self, stations_df):
        """
        Generate HTML with station dropdown
        """
        # Convert stations to option elements
        options = ""
        for _, row in stations_df.iterrows():
            options += f'<option value="{row["stop_id"]}">{row["stop_name"]}</option>\n'

        # Create the complete HTML
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metro Transit Map</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }}
        
        .header {{
            background-color: #f8f9fa;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .station-select {{
            width: 100%;
            max-width: 400px;
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
            background-color: white;
            cursor: pointer;
        }}

        .station-select:hover {{
            border-color: #999;
        }}

        .station-select:focus {{
            outline: none;
            border-color: #0066cc;
            box-shadow: 0 0 0 2px rgba(0,102,204,0.2);
        }}

        .map-container {{
            height: calc(100vh - 70px);
            background-color: #eee;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <select class="station-select" id="stationSelect">
            <option value="">Select a station...</option>
            {options}
        </select>
    </div>

    <div class="map-container">
        <p>Map will go here</p>
    </div>

    <script>
        // Store station data for use in JavaScript
        const stationData = {json.dumps(stations_df.to_dict('records'))};
        
        document.getElementById('stationSelect').addEventListener('change', function() {{
            const selectedStation = this.value;
            if (selectedStation) {{
                console.log('Selected station:', selectedStation);
                const stationInfo = stationData.find(station => station.stop_id === selectedStation);
                console.log('Station info:', stationInfo);
                // Add your station selection handling code here
            }}
        }});
    </script>
</body>
</html>
        """
        
        return html
    
    def save_html(self, html_content, output_path='../pages/index.html'):
        """
        Save the generated HTML to a file
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"HTML file saved to {output_path}")
        except Exception as e:
            print(f"Error saving HTML: {e}")

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