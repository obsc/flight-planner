import greatcircle, sets, csv, pandas, distance
from shapely.geometry import LineString, Polygon
no_fly_zones = []

def populateNoFlyZones():
  zones = pandas.read_csv('../basicAgent/restrictedZones.csv')
  vertices = zones['LatLongVertices']
  points = [[[float(x) for x in c.split(':')] for c in l.split(' ')] for l in vertices]
  polygons = [Polygon(x) for x in points]
  global no_fly_zones
  no_fly_zones = polygons
populateNoFlyZones()

def getSpecDist(pt1, pt2):
  line = LineString([pt1, pt2])
  for zone in no_fly_zones:
    if line.intersects(zone):
      return float('inf')
    else:
      pass
  return greatcircle.get_dist(pt1,pt2)

def pathDist(path):
  sum = 0
  for i in range(0, len(path)-1):
    sum += greatcircle.get_dist(path[i],path[i+1])
  return sum

def getNodes(start, goal, spread = 100):
  lat1, lon1 = start
  lat2, lon2 = goal
  lat_interval = (lat2 - lat1)/spread
  lon_interval = (lon2 - lon1)/spread
  nodes = []
  for i in range(1, spread+1):
    for j in range(1, spread+1):
      nodes.append((lat1 + i * lat_interval, lon1 + j * lon_interval))
  x = nodes[0:len(nodes)-1]
  x.append(goal)
  return x

def airport_path(AirportID1, AirportID2, spread):
  start = distance.airportToLatLon(AirportID1)
  goal = distance.airportToLatLon(AirportID2)
  path = a_star(start, goal, spread)
  print str(pathDist(path))
  print str(greatcircle.get_dist(start, goal))
  return path

def a_star(start, goal, spread):
  nodes = getNodes(start, goal, spread)
  def heur(x):
    try: 
      return greatcircle.get_dist(x, goal)
    except ValueError:
      return 0.0
  def pointEquals(x, y):
    x1, x2 = x
    y1, y2 = y
    return abs(y1-x1)<0.000001 and abs(y2-x2)<0.000001
  closedSet = sets.Set()
  openSet = sets.Set()
  openSet.add(start)
  cameFrom = dict()
  f_score = dict()
  g_score = dict()
  g_score[start] = 0
  f_score[start] = g_score[start] + heur(start)
  prev = start
  while len(openSet) != 0:
    current = None
    for node in openSet:
      if current == None:
        current = node
      else:
        if f_score[node] < f_score[current]:
          current = node
        else:
          pass
    if pointEquals(current,goal):
      path = [goal]
      while current != start:
        prev = cameFrom[current]
        current = prev
        path.append(prev)
      return path[::-1]
    openSet.remove(current)
    closedSet.add(current)
    for neighbor in nodes:
      if neighbor == current:
        pass
      else:
        tent_gscore = g_score[current] + getSpecDist(current, neighbor)
        tent_fscore = tent_gscore + heur(neighbor)
        if neighbor in closedSet and tent_fscore >= f_score[neighbor]:
          continue
        elif neighbor not in openSet or tent_fscore < f_score[neighbor]:
          cameFrom[neighbor] = current
          g_score[neighbor] = tent_gscore
          f_score[neighbor] = tent_fscore
          if neighbor not in openSet:
            openSet.add(neighbor)
