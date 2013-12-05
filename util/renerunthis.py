import astar, distance, pickle

def getPaths(outfile):
  f = open('dat/AirportsLatLong.csv')
  f.readline()
  airports = []
  for line in f:
    stuff = line.split(',')
    airportID = stuff[0]
    lat, lon = (float(stuff[1]),float(stuff[2]))
    airports.append(airportID)
  f.close()
  path_dict = dict()
  for i in range(0, len(airports)):
    for j in range(0, len(airports)):
      if i == j:
        pass
      else:
        id1= airports[i]
        id2= airports[j]
        refinement = 10
        path = astar.airport_path(id1, id2, refinement)
        path_dist = astar.pathDist(path)
        opt_dist = distance.airportDistance(id1, id2)
        if path_dist / opt_dist > 1.05:
          refinement += 5
          path = astar.airport_path(id1, id2, refinement)
          path_dist = astar.pathDist(path)
          if refinement > 50:
            break
        print str(path_dist/opt_dist)
        path_dict[(id1,id2)] = path
  f = open(outfile, 'w')
  pickle.dump(path_dict, outfile)
