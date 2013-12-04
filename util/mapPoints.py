from math import atan2, sin, cos
import sets

def calcBearing(lat1, lon1, lat2, lon2):
  lon_diff = lon2 - lon1
  bearing = atan2( sin(lon_diff) * cos(lat2), cos(lat1) * sin(lat2) -sin(lat1)*cos(lat2)*cos(lon_diff))
  return bearing

def mapToVectors(asdipositionsorted, sortedFlightHistory, airportFile, outfile):
  f = open(asdipositionsorted)
  g = open(outfile, 'w')
  validAirportSet = validAirports(airportFile)
  g.write('FlightHistoryID,Time,Latitude,Longitude,Angle,Bearing,NextLat,NextLon,Airport,Altitude,Speed\n')
  airport_dict = mapToDestination(sortedFlightHistory)
  line = f.readline()
  stuff = line.strip().split(',')
  curFHID = stuff[7]
  lat = float(stuff[5])
  lon = float(stuff[6])
  time = stuff[1]
  speed = int(stuff[4])
  altitude = int(stuff[3])
  for line in f:
    stuff =line.strip().split(',')
    try:
      if stuff[7] == curFHID:
        bearing = calcBearing(lat, lon, float(stuff[5]), float(stuff[6]))
        angle = atan2(float(stuff[5]) - lat, float(stuff[6]) - lon)
        g.write('%s,%s,%f,%f,%f,%f,%f,%f,%s,%i,%i\n' % (curFHID, time, lat, lon, angle,bearing,float(stuff[5]),float(stuff[6]),airport_dict[curFHID], altitude, speed))
      else:
        pass
      if stuff[7] in validAirportSet:
        curFHID = stuff[7]
        lat = float(stuff[5])
        lon = float(stuff[6])
        time = stuff[1]
        speed = int(stuff[4])
        altitude = int(stuff[3])
      else:
        pass
    except ValueError:
      print 'GODDAMMIT'
  f.close()
  g.close()

def mapToDestination(sortedFlightHistory):
  f = open(sortedFlightHistory)
  f.readline()
  fhid_dict = dict()
  for line in f:
    try:
      stuff = line.strip().split(',')
      fhid = stuff[0]
      airport = stuff[7]
      fhid_dict[fhid] = airport
    except ValueError:
      print 'FUUUUUCK'
  f.close()
  print 'done'
  return fhid_dict

def validAirports(airportFile):
  return_set = sets.Set()
  f = open(airportFile)
  f.readline()
  for line in f:
    stuff = line.strip().split(',')
    airportID = stuff[0]
    return_set.add(airportID)
  f.close()
  return return_set
