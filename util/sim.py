import greatcircle
import math
'''
  arrays in form [lat, lon, bearing]
'''
def KNNsim(x,y):
  dist = greatcircle.get_dist((x[0],x[1]),(y[0],y[1])) + 0.00001
  bearing1 = x[2] if x[2] > 0 else 2 * math.pi - x[2]
  bearing2 = y[2] if y[2] > 0 else 2 * math.pi - y[2]
  angle_diff_inverse = abs(bearing2-bearing1) if abs(bearing2-bearing1) > 0 else 0.00001
  return angle_diff_inverse * dist

def KNNeuclid(x,y):
  return greatcircle.get_dist((x[0],x[1]),(y[0],y[1]))

'''
  arrays in form [lat,lon,bearing,altitude]
'''
def KNNasim(x,y):
  return KNNsim(x,y) * altSim(x[3], y[3])

def altSim(x,y):
  x = math.fabs(math.log(float(x)/y))
  return 1 + x
