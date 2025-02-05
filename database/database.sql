-- table that will allocate the grouped_result
--

CREATE TABLE gropued_result (
    stop_id VARCHAR(50),
    stop_headsign VARCHAR(100),
    arrival_time TIME
);

-- Creating tables for the provided transit data files

CREATE TABLE agency (
    agency_id TEXT PRIMARY KEY,
    agency_name TEXT NOT NULL,
    agency_url TEXT NOT NULL,
    agency_timezone TEXT NOT NULL,
    agency_lang TEXT
);

CREATE TABLE calendar (
    service_id TEXT PRIMARY KEY,
    monday INTEGER NOT NULL,
    tuesday INTEGER NOT NULL,
    wednesday INTEGER NOT NULL,
    thursday INTEGER NOT NULL,
    friday INTEGER NOT NULL,
    saturday INTEGER NOT NULL,
    sunday INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

CREATE TABLE calendar_dates (
    service_id TEXT NOT NULL,
    date DATE NOT NULL,
    exception_type INTEGER NOT NULL,
    PRIMARY KEY (service_id, date)
);

CREATE TABLE fare_attributes (
    fare_id TEXT PRIMARY KEY,
    price REAL NOT NULL,
    currency_type TEXT NOT NULL,
    payment_method INTEGER NOT NULL,
    transfers INTEGER,
    transfer_duration INTEGER
);

CREATE TABLE fare_rules (
    fare_id TEXT NOT NULL,
    route_id TEXT,
    origin_id TEXT,
    destination_id TEXT,
    PRIMARY KEY (fare_id, origin_id, destination_id)
);

CREATE TABLE feed_info (
    feed_publisher_name TEXT NOT NULL,
    feed_publisher_url TEXT NOT NULL,
    feed_lang TEXT NOT NULL,
    default_lang TEXT,
    feed_start_date DATE,
    feed_end_date DATE,
    feed_version TEXT,
    feed_contact_email TEXT
);

CREATE TABLE frequencies (
    trip_id TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    headway_secs INTEGER NOT NULL,
    PRIMARY KEY (trip_id, start_time)
);

CREATE TABLE routes (
    route_id TEXT PRIMARY KEY,
    agency_id TEXT,
    route_short_name TEXT,
    route_long_name TEXT,
    route_desc TEXT,
    route_type INTEGER NOT NULL,
    route_url TEXT,
    route_color TEXT
);

CREATE TABLE stops (
    stop_id TEXT PRIMARY KEY,
    stop_name TEXT NOT NULL,
    stop_desc TEXT,
    stop_lat REAL NOT NULL,
    stop_lon REAL NOT NULL,
    zone_id TEXT,
    stop_url TEXT,
    location_type INTEGER,
    parent_station TEXT
);

CREATE TABLE stop_times (
    trip_id TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    departure_time TEXT NOT NULL,
    stop_id TEXT NOT NULL,
    stop_sequence INTEGER NOT NULL,
    stop_headsign TEXT,
    pickup_type INTEGER,
    drop_off_type INTEGER,
    shape_dist_traveled REAL,
    PRIMARY KEY (trip_id, stop_id, stop_sequence)
);

CREATE TABLE transfers (
    from_stop_id TEXT NOT NULL,
    to_stop_id TEXT NOT NULL,
    transfer_type INTEGER NOT NULL,
    min_transfer_time INTEGER,
    PRIMARY KEY (from_stop_id, to_stop_id)
);

CREATE TABLE trips (
    route_id TEXT NOT NULL,
    service_id TEXT NOT NULL,
    trip_id TEXT PRIMARY KEY,
    trip_headsign TEXT,
    direction_id INTEGER,
    block_id TEXT,
    shape_id TEXT
);
