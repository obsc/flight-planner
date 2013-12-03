from math import sin, cos, atan2, sqrt

airportDict = dict()

def genAirportDict():
  with open('dat/AirportsLatLong.csv') as f:
    f.readline()
    for line in f:
      stuff = line.split(',')
      airportID = stuff[0]
      lat, lon = (float(stuff[1]),float(stuff[2]))
      airportDict[airportID] = (lat, lon)

genAirportDict()

class InvalidAirport(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

'return distance between two points in km'
def distance(lat1, lon1, lat2, lon2):
  a = (sin(lat2 - lat1))**2.0 + cos(lat1) * cos(lat2) * (sin(lon2-lon1)/2.)**2.0
  c = 2 * atan2(sqrt(a), sqrt(1-a))
  return 6371 * c #6371 radius of earth in km

def airportToLatLon(airportID):
  if airportID in airportDict:
    return airportDict[airportID]
  else:
    raise InvalidAirport(airportID + ' was not founds')

def airportDistance(airportID1, airportID2):
  lat1, lon1 = airportToLatLon(airportID1)
  lat2, lon2 = airportToLatLon(airportID2)
  return distance(lat1,lon1,lat2,lon2)

def distanceToAirport(lat1, lon1, airportID):
  lat2, lon2 = airportToLatLon(airportID)
  return distance(lat1, lon1, lat2, lon2)