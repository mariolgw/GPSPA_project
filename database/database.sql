-- Create table for stops
CREATE TABLE stops (
    stop_id VARCHAR(50) PRIMARY KEY,
    stop_lat DECIMAL(9, 6),
    stop_lon DECIMAL(9, 6)
);

-- Create table for arrival times
CREATE TABLE arrival_times (
    stop_id VARCHAR(50),
    stop_headsign VARCHAR(100),
    arrival_time TIME,
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);

-- Create table for station info
CREATE TABLE station_info (
    stop_id VARCHAR(50),
    trip_id VARCHAR(50),
    stop_url TEXT,
    stop_headsign VARCHAR(100),
    route_short_name VARCHAR(10),
    route_long_name VARCHAR(50),
    route_color VARCHAR(10),
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);