import csv
import greatcircle

def load_paths():
    f = csv.reader(open("dat/sampleSubmission.csv"))
    g = csv.reader(open("dat/TestFlights.csv"))
    f.next()
    g.next()

    paths = {}
    for row in g:
        # latitude, longitude, altitude, speed
        start = (float(row[4]), float(row[5]), int(row[6]), int(row[7]))
        paths[int(row[0])] = [start]

    for row in f:
        pos = (float(row[2]), float(row[3]), int(row[4]), int(row[5]))
        paths[int(row[0])].append(pos)

    return paths

def expand_path(path, n):
    prev = None
    dists = []
    for pos in path:
        if prev is not None:
            (px, py, palt, pspd) = prev
            (cx, cy, calt, cspd) = pos
            dists.append(greatcircle.get_dist((px,py),(cx,cy)))
        prev = pos
    totalDist = sum(dists)
    print totalDist

def expand_paths(paths, n):
    for k in paths.keys():
        expand_path(paths[k], n)

def paths_to_waypoints(paths):
    waypoints = []
    keys = paths.keys()
    keys.sort()
    for flightId in keys:
        i = 0
        for (lat, lon, alt, spd) in paths[flightId]:
            if i != 0:
                waypoints.append([flightId, i, lat, lon, alt, spd])
            i += 1
    return waypoints

def write_file(f, waypoints):
    waypoints_header = ["FlightId", "Ordinal", "Latitude", "Longitude", "Altitude", "AirSpeed"]
    waypoints.insert(0, waypoints_header)
    writer = csv.writer(open(f,'w'), lineterminator='\n')
    writer.writerows([[str(x) for x in waypoint] for waypoint in waypoints])

if __name__ == "__main__":
    paths = load_paths()
    expand_paths(paths, 100)
    waypoints = paths_to_waypoints(paths)
    write_file("dat/output.csv", waypoints)
