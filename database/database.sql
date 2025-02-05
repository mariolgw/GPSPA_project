-- table that will allocate the grouped_result
CREATE TABLE gropued_result (
    stop_id VARCHAR(50),
    stop_headsign VARCHAR(100),
    arrival_time TIME
);

-- table that will allocate the stations
CREATE TABLE stations (
    stop_id VARCHAR(50),
    stop_name VARCHAR(100),
    stop_lat FLOAT,
    stop_lon FLOAT
);
