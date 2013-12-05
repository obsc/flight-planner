import greatcircle
import math
'''
  arrays in form [lat, lon, bearing]
'''
def KNNsim(x,y):
  dist = greatcircle.get_dist((x[0],x[1]),(y[0],y[1]))
  angle_diff_inverse = 2* math.pi - abs(x[2]-y[2])
  return bearing * dist

def KNNeuclid(x,y):
  return greatcircle.get_dist((x[0],x[1]),(y[0],y[1]))

'''
  arrays in form [lat,lon,bearing,altitude]
'''
def KNNasim(x,y):
  return KNNsim(x,y) * altSim(x, y)

def altSim(x,y):
  x = math.fabs(math.log(float(x)/y))
  x = 0 if x >3.14 else x
  return math.cos(x)
