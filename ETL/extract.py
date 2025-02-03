#import necessary packages

import pandas as pd

#load the data

agency = pd.read_csv('../data/agency.txt')
cal_dates = pd.read_csv('../data/calendar_dates.txt')
calendar = pd.read_csv('../data/calendar.txt')
fare_attr = pd.read_csv('../data/fare_attributes.txt')
fare_rules = pd.read_csv('../data/fare_rules.txt')
feed_info = pd.read_csv('../data/feed_info.txt')
frequencies = pd.read_csv('../data/frequencies.txt')
routes = pd.read_csv('../data/routes.txt')
stop_times = pd.read_csv('../data/stop_times.txt')
stops = pd.read_csv('../data/stops.txt')
transfers = pd.read_csv('../data/transfers.txt')
trips = pd.read_csv('../data/trips.txt')

# this is the "motherload". This is the schedule for each trip and will help us make the schedule at each 
# station for each day. 

stop_times = stop_times.drop(columns=['pickup_type','drop_off_type','shape_dist_traveled'])
stops = stops.drop(columns=['stop_desc','stop_url','zone_id','location_type'])

single_line_stations = [
    "AF", "AH", "AL", "AS", "AX", "AN", "AE", "AR", "AV", 
    "BV", "CR", "CS", "CP", "CA", "CH", "CU", "CM", "EC", 
    "IN", "JZ", "LA", "LU", "MP", "MM", "OD", "OL", "OS", 
    "OR", "PA", "PI", "PO", "PE", "QC", "RA", "RE", "RM", 
    "RO", "SP",  "SR", "TE", "TP", "MO", "EN", "AP", "RB"
]

unique_directions = stop_times["stop_headsign"].unique()

# Function to modify stop_id for single-line stations
def modify_stop_times(row):
    if row["stop_id"] in single_line_stations:
        direction = row["stop_headsign"].replace(" ", "_")  # Extract direction
        row["stop_id"] = f"{row['stop_id']}_{direction}"  # Append direction
    return row

# Apply modification
stop_times = stop_times.apply(modify_stop_times, axis=1)

# 2️ Modify `stops` to match the new stop_ids created in `stop_times`
stops_expanded = []
for _, row in stops.iterrows():
    if row["stop_id"] in single_line_stations:
        for direction in unique_directions:
            stops_expanded.append(row.to_dict() | {"stop_id": f"{row['stop_id']}_{direction.replace(' ', '_')}"})
    else:
        stops_expanded.append(row.to_dict())

stops = pd.DataFrame(stops_expanded)  # Convert expanded list back to DataFrame

# 3️ Merge the modified `stops` and `stop_times`
result = pd.merge(stops, stop_times, on="stop_id", how="inner")


# 4️ Group by stop_id & stop_headsign to separate schedules per direction
grouped_result = result.groupby(["stop_id", "stop_headsign"]).agg({
    "arrival_time": list,
}).reset_index()

grouped_result = grouped_result.sort_values('stop_headsign')

#creating a single file that combines the stations with the trains that pass through them
grouped_result.to_csv("ETL/data/grouped_result_fixed.txt", sep="\t", index=False)

#Just missing the end line stations that instead of having arrival time will have departure time

