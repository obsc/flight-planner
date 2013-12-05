SELECT *
FROM (SELECT * FROM flight_planner.flight_history where id = 306898411 ) a
INNER JOIN flight_planner.flight_plan b ON a.id = b.flighthistory_id and a.departure_airport_code = b.departure_airport and a.arrival_airport_code = b.arrival_airport;
INNER JOIN flight_planner.way_points wp ON wp.asdiflightplan_id = b.id
ORDER BY b.id, wp.ORDINAL;


--QUERY FOR PYTHON OUTPUT
SELECT fh.ID as FLIGHT_ID, 
		wp.LATITUDE, wp.LONGITUDE, 
       ((fp.ORIGINAL_ARRIVAL_UTC - fp.ESTIMATED_ARRIVAL_UTC) - (fp.ORIGINAL_DEPARTURE_UTC - fp.ESTIMATED_DEPARTURE_UTC)) AS DELAY_COST, 
       ACTUAL_RUNWAY_DEPARTURE AS TIME_OF_TRAVEL, 
       ORDINAL AS NEXT_HOP
FROM TRUNCATED_FLIGHT_HISTORY fh
INNER JOIN TRUNCATED_FLIGHT_PLAN fp ON fh.ID = fp.flighthistory_id
INNER JOIN truncated_way_points wp ON wp.asdiflightplan_id = fp.id;