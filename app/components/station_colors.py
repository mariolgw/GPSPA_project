import pandas as pd
import json

def generate_stop_info(stops_path, stop_times_path, output_path=None):
    # Load data
    stops = pd.read_csv(stops_path)
    stop_times = pd.read_csv(stop_times_path)

    # Merge stops and stop_times dataframes
    stops_with_times = pd.merge(stops, stop_times, on='stop_id')

    # Get unique stop names
    unique_stop_names = stops_with_times['stop_name'].unique()

    # Create a dictionary to store the results
    stop_info = {}

    # Iterate over each unique stop name
    for stop_name in unique_stop_names:
        # Filter the stops_with_times dataframe for the current stop name
        filtered_stops = stops_with_times[stops_with_times['stop_name'] == stop_name]

        # Group by stop_id and select the first trip_id for each stop_id
        grouped_stops = filtered_stops.groupby('stop_id').first().reset_index()

        # Extract the required columns
        stop_info[stop_name] = grouped_stops[['stop_id', 'trip_id', 'stop_url', 'stop_headsign']].to_dict(orient='records')

    # Convert the dictionary to a JSON string
    stop_info_json = json.dumps(stop_info, indent=4)

    # Save to file if output_path is provided
    if output_path:
        with open(output_path, 'w') as json_file:
            json_file.write(stop_info_json)

    return stop_info_json

# Example usage
if __name__ == "__main__":
    stops_path = 'data/stops.txt'
    stop_times_path = 'data/stop_times.txt'
    output_path = 'app/components/station_info.json'
    stop_info_json = generate_stop_info(stops_path, stop_times_path, output_path)
    #print(stop_info_json)