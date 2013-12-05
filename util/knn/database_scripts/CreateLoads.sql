CREATE DATABASE FLIGHT_PLANNER;

DROP TABLE FLIGHT_PLANNER.POSITION;
CREATE TABLE FLIGHT_PLANNER.POSITION (
   id INTEGER,
   received datetime,
   callsign VARCHAR(10),
   altitude INTEGER,
   ground_speed INTEGER,
   latitude_degrees DECIMAL(15,10),
   longitude_degrees DECIMAL(15,10),
   flighthistory_id INTEGER
);

LOAD DATA LOCAL INFILE "D:\\Cornell\\4780ML\\flight\\flight-planner\\data\\GEKaggle\\TTrain\\training2_asdiposition.csv"
INTO TABLE FLIGHT_PLANNER.POSITION
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;


DROP TABLE FLIGHT_PLANNER.FLIGHT_HISTORY;
CREATE TABLE FLIGHT_PLANNER.FLIGHT_HISTORY (
	id INTEGER,
	airline_code VARCHAR(10),
	irline_icao_code VARCHAR(40),
	flight_number INTEGER,
	departure_airport_code VARCHAR(10),
	departure_airport_icao_code VARCHAR(10),
	arrival_airport_code VARCHAR(10),
	arrival_airport_icao_code VARCHAR(10),
	published_departure DATETIME,
	published_arrival datetime,
	scheduled_gate_departure datetime,
	actual_gate_departure datetime,
	scheduled_gate_arrival datetime,
	actual_gate_arrival datetime,
	scheduled_runway_departure datetime,
	actual_runway_departure datetime,
	scheduled_runway_arrival datetime,
	actual_runway_arrival datetime,
	creator_code varchar(10),
	scheduled_air_time integer,
	scheduled_block_time integer,
	departure_airport_timezone_offset integer,
	arrival_airport_timezone_offset integer,
	scheduled_aircraft_type varchar(20),
	actual_aircraft_type varchar(20),
	icao_aircraft_type_actual varchar(20)
);

LOAD DATA LOCAL INFILE "D:\\Cornell\\4780ML\\flight\\flight-planner\\data\\GEKaggle\\TTrain\\training2_flighthistory.csv"
INTO TABLE FLIGHT_PLANNER.FLIGHT_HISTORY
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

DROP TABLE flight_planner.airports;
create table flight_planner.airports (
	airport varchar(10),
	latitude DECIMAL(15,10),
	longitude decimal(15, 10),
	elevation decimal(10, 4),
	radius decimal(15, 5),
	height decimal(10, 4)
);

LOAD DATA LOCAL INFILE "D:\\Cornell\\4780ML\\flight\\flight-planner\\util\\dat\\AirportsLatLong.csv"
INTO TABLE FLIGHT_PLANNER.airports
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

DROP TABLE flight_planner.flight_plan;
CREATE TABLE flight_planner.flight_plan (
	id INTEGER,
	update_time_utc datetime,
	flighthistory_id INTEGER,
	departure_airport VARCHAR(10),
	arrival_airport varchar(10),
	aircraft_id varchar(10),
	legacy_route varchar(1000),
	original_departure_utc datetime,
	estimated_departure_utc datetime,
	original_arrival_utc datetime,
	estimated_arrival_utc datetime
);

LOAD DATA LOCAL INFILE "D:\\Cornell\\4780ML\\flight\\flight-planner\\data\\GEKaggle\\TTrain\\training2_asdiflightplan.csv"
INTO TABLE FLIGHT_PLANNER.flight_plan
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

ALTER TABLE FLIGHT_PLANNER.FLIGHT_HISTORY ADD primary key(id);
ALTER TABLE FLIGHT_PLANNER.flight_plan ADD primary key(id);

ALTER TABLE FLIGHT_PLANNER.flight_plan
ADD constraint FlightPlan_FlightHistory_FK
FOREIGN KEY (flighthistory_id)
references flight_planner.FLIGHT_HISTORY(id);

DROP TABLE flight_planner.way_points;
CREATE TABLE flight_planner.way_points (
	id INTEGER,
	asdiflightplan_id INTEGER,
	ordinal INTEGER,
	latitude DECIMAL(15,10),
	longitude DECIMAL(15, 10)
);


ALTER TABLE FLIGHT_PLANNER.way_points ADD primary key(id);

ALTER table flight_planner.way_points
add constraint WayPoints_FlightPlan_FK
FOREIGN KEY (asdiflightplan_id)
references flight_planner.flight_plan(id);

LOAD DATA LOCAL INFILE "D:\\Cornell\\4780ML\\flight\\flight-planner\\data\\GEKaggle\\TTrain\\training2_asdifpwaypoint.csv"
INTO TABLE FLIGHT_PLANNER.way_points
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES;



--   These are for testing

DROP TABLE flight_planner.truncated_way_points;
DROP TABLE flight_planner.TRUNCATED_FLIGHT_PLAN;
DROP TABLE FLIGHT_PLANNER.TRUNCATED_FLIGHT_HISTORY;


CREATE TABLE FLIGHT_PLANNER.TRUNCATED_FLIGHT_HISTORY (
	id INTEGER PRIMARY KEY,
	airline_code VARCHAR(10),
	irline_icao_code VARCHAR(40),
	flight_number INTEGER,
	departure_airport_code VARCHAR(10),
	departure_airport_icao_code VARCHAR(10),
	arrival_airport_code VARCHAR(10),
	arrival_airport_icao_code VARCHAR(10),
	published_departure DATETIME,
	published_arrival datetime,
	scheduled_gate_departure datetime,
	actual_gate_departure datetime,
	scheduled_gate_arrival datetime,
	actual_gate_arrival datetime,
	scheduled_runway_departure datetime,
	actual_runway_departure datetime,
	scheduled_runway_arrival datetime,
	actual_runway_arrival datetime,
	creator_code varchar(10),
	scheduled_air_time integer,
	scheduled_block_time integer,
	departure_airport_timezone_offset integer,
	arrival_airport_timezone_offset integer,
	scheduled_aircraft_type varchar(20),
	actual_aircraft_type varchar(20),
	icao_aircraft_type_actual varchar(20)
);


CREATE TABLE flight_planner.TRUNCATED_FLIGHT_PLAN (
	id INTEGER PRIMARY KEY,
	update_time_utc datetime,
	flighthistory_id INTEGER,
	departure_airport VARCHAR(10),
	arrival_airport varchar(10),
	aircraft_id varchar(10),
	legacy_route varchar(1000),
	original_departure_utc datetime,
	estimated_departure_utc datetime,
	original_arrival_utc datetime,
	estimated_arrival_utc datetime,
	FOREIGN KEY(flighthistory_id) references flight_planner.truncated_flight_history(id)
	ON DELETE CASCADE
);


CREATE TABLE flight_planner.truncated_way_points (
	id INTEGER PRIMARY KEY,
	asdiflightplan_id INTEGER,
	ordinal INTEGER,
	latitude DECIMAL(15,10),
	longitude DECIMAL(15, 10),
	foreign key (asdiflightplan_id) references FLIGHT_PLANNER.truncated_flight_plan(id)
	ON DELETE CASCADE
);

insert into FLIGHT_PLANNER.TRUNCATED_FLIGHT_HISTORY
select * from flight_planner.flight_history
where id in (SELECT DISTINCT flighthistory_id FROM flight_planner.flight_plan fp
INNER JOIN (select DISTINCT asdiflightplan_id from (SELECT * FROM flight_planner.way_points LIMIT 10000) c) wp on fp.ID = wp.asdiflightplan_id);

insert into flight_planner.truncated_flight_plan
select * from flight_planner.flight_plan
where flighthistory_id in (SELECT ID from FLIGHT_PLANNER.TRUNCATED_FLIGHT_HISTORY);

INSERT INTO FLIGHT_PLANNER.truncated_WAY_POINTS
(SELECT * FROM flight_planner.way_points LIMIT 10000);

