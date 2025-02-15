import requests

def get_station_info(stop_id):
    """Get information about a specific station."""
    url = f'http://localhost:3000/station/{stop_id}'
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            station = response.json()
            print(f"Station Name: {station['stop_name']}")
            print(f"Location: {station['stop_lat']}, {station['stop_lon']}")
        else:
            print("Station not found or error occurred")
            
    except requests.RequestException as e:
        print(f"Error connecting to the server: {e}")

# Example usage
get_station_info('DEMO1')  # Replace with your actual stop_id