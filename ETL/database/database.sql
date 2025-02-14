-- 1. Create table for stops first
CREATE TABLE stops (
    stop_id VARCHAR(50) PRIMARY KEY,
    stop_headsign VARCHAR(100),
    stop_lat DECIMAL(9, 6),
    stop_lon DECIMAL(9, 6),
    geom geometry(POINT, 4326) -- Geometry column for spatial data
);

-- 2. Create the function to populate the geom column
CREATE OR REPLACE FUNCTION create_geom()
RETURNS TRIGGER AS
$$
BEGIN
    NEW.geom := ST_SetSRID(ST_MakePoint(NEW.stop_lon, NEW.stop_lat), 4326);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 3. Create the trigger AFTER the stops table exists
CREATE TRIGGER insert_rides_in_pa
BEFORE INSERT ON stops
FOR EACH ROW
EXECUTE FUNCTION create_geom();

-- 4. Create table for departure times
CREATE TABLE departure_times (
    id SERIAL PRIMARY KEY, -- Unique identifier for each row
    weekday VARCHAR(10) NOT NULL, -- WKDY, SAT, SUN, etc.
    stop_id VARCHAR(50) NOT NULL, -- FK reference to the stops table
    departure_time TIME NOT NULL, -- Valid time for each stop
    stop_headsign VARCHAR(100) NOT NULL, -- Consistent with station_info
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);

-- 5. Create table for station info
CREATE TABLE station_info (
    stop_id VARCHAR(50) PRIMARY KEY,
    trip_id VARCHAR(50),
    stop_url TEXT,
    stop_headsign VARCHAR(100),
    route_short_name VARCHAR(10),
    route_long_name VARCHAR(50),
    route_color VARCHAR(10),
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);
