-- Create table for stops
CREATE TABLE stops (
    stop_id VARCHAR(50) PRIMARY KEY,
    stop_name VARCHAR(100),
    stop_lat DECIMAL(9, 6),
    stop_lon DECIMAL(9, 6),
    geom geometry(POINT, 4326)
);

-- Create table for arrival times
CREATE TABLE departure_times (
    id SERIAL PRIMARY KEY, -- Unique identifier for each row
    weekday VARCHAR(10) NOT NULL, -- WKDY, SAT, SUN, etc.
    stop_id VARCHAR(50) NOT NULL, -- FK reference to the stops table
    departure_time TIME NOT NULL, -- Valid time for each stop
    stop_headsign VARCHAR(100) NOT NULL, -- Consistent with station_info
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);

-- Create table for station info
CREATE TABLE station_info (
    stop_id VARCHAR(50) PRIMARY key,
    trip_id VARCHAR(50),
    stop_url TEXT,
    stop_headsign VARCHAR(100),
    route_short_name VARCHAR(10),
    route_long_name VARCHAR(50),
    route_color VARCHAR(10),
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id)
);


CREATE Or REPLACE FUNCTION create_geom()
RETURNS TRIGGER AS
$$
BEGIN
	new.geom :=	ST_SetSRID(ST_MakePoint(new.stop_lon, new.stop_lat), 4326);
	RETURN new;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER insert_rides_in_pa
AFTER INSERT ON stops
FOR EACH ROW
EXECUTE PROCEDURE create_geom();