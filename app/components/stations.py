import pandas as pd
import json

data_path = '/Users/mario/Documents/NOVA IMS/Winter Semester/Group Project Seminar on Programming and Analysis/Group Project/GPSPA_project/data'
class StationListGenerator:
    
    def get_stations(self):
        """
        Get stations names for frontend
        """
        
        # Load data
        stops = pd.read_csv(f'{data_path}/stops.txt')
        
        # Get unique stations
        stations = stops['stop_name'].unique()
        
        return stations
    
    def save_stations_as_json(self, stations, output_path):
        """
        Save stations names as JSON
        """
        with open(output_path, 'w') as json_file:
            json.dump(stations.tolist(), json_file)

def main():
    generator = StationListGenerator()
    
    # Get stations
    stations = generator.get_stations()

    # Save stations as JSON
    if stations.size > 0:
        generator.save_stations_as_json(stations, 'app/components/stations.json')

if __name__ == "__main__":
    main()