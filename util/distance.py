from math import atan, sin, cos, atan2, sqrt, asin, tan
import greatcircle


airportDict = dict()

def genAirportDict():
  with open('AirportsLatLong.csv') as f:
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


def airportToLatLon(airportID):
  if airportID in airportDict:
    return airportDict[airportID]
  else:
    raise InvalidAirport(airportID + ' was not founds')

def airportDistance(airportID1, airportID2):
  lat1, lon1 = airportToLatLon(airportID1)
  lat2, lon2 = airportToLatLon(airportID2)
  return greatcircle.get_dist((lat1,lon1),(lat2,lon2))

def distanceToAirport(lat1, lon1, airportID):
  lat2, lon2 = airportToLatLon(airportID)
  return greatcircle.get_dist((lat1, lon1), (lat2, lon2))