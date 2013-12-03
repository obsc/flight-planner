from math import atan, sin, cos, atan2, sqrt, asin, tan


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

'''
def distance2(lat1, lon1, lat2, lon2):
  beta_1 = atan(tan(lat1))
  beta_2 = atan(tan(lat2))
  P = (beta_1 + beta_2)/2.0
  Q = (beta_2 - beta_1)/2.0
  centralAngle = 2 * asin(sqrt(sin((lat2-lat1)/2)**2. + cos(lat1) * cos(lat2) * (sin((lon2-lon1)/2))**2.))
  X = (centralAngle - sin(centralAngle)) * (sin(P)*cos(Q))**2 / ((cos(centralAngle/2))**2.)
  Y = (centralAngle + sin(centralAngle)) * (cos(P) * sin(Q))**2 / (sin(centralAngle/2))**2
  a = 6371
  distance = a * (centralAngle - (.5)*(X+Y))
  return distance 
'''

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