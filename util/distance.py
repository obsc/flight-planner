from math import sin, cos, atan2

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
  f = open('dat/AirportsLatLong.csv')
  f.readline()
  for line in f:
    stuff = line.split(',')
    if stuff[0] == airportID:
      lat = float(stuff[1])
      lon = float(stuff[2])
      return (lat, lon)
    else:
      pass
  raise InvalidAirport(airportID + ' was not founds')

def airportDistance(airportID1, airportID2):
  lat1, lon1 = airportToLatLon(airportID1)
  lat2, lon2 = airportToLatLon(airportID2)
  return distance(lat1,lon1,lat2,lon2)

def distanceToAirport(lat1, lon1, airportID):
  lat2, lon2 = airportToLatLon(airportID)
  return distance(lat1, lon1, lat2, lon2)