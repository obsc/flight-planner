import csv
import greatcircle

SPLITNUM = 32

def load_paths():
  f = csv.reader(open("dat/IMPORTANTHASHTAG.csv"))
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
  n = n - len(dists)
  newPath = [path[0]]
  for i in xrange(len(dists)):
    split = int(n * (dists[i] / totalDist))
    (sx, sy, salt, sspd) = path[i]
    (ex, ey, ealt, espd) = path[i + 1]
    start = (sx, sy)
    end = (ex, ey)

    posList = greatcircle.get_path(start, end, split + 1)
    for i in xrange(len(posList)):
      (x,y) = posList[i]
      alt = ealt
      spd = espd
      posList[i] = (x,y,alt,spd)

    newPath = newPath + posList[1:]

  return newPath

def expand_paths(paths, n):
  for k in paths.keys():
    paths[k] = expand_path(paths[k], n)

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
  expand_paths(paths, SPLITNUM)
  waypoints = paths_to_waypoints(paths)
  write_file("dat/splitBase.csv", waypoints)
