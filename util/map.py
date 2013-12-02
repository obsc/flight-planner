
def mapToMaxAltSpeed():
  f= open('whatever')
  f.readline()
  g = open('whateve','w')
  line = f.readline()
  line = line.split{','}
  flightHistID = line[0]
  flightSpeed = float(line[1])
  flightAltitude = float(line[2])
  for line in f:
    line = line.split(',')
    if line[0] == flightHistID:
      flightSpeed = max(flightSpeed, float(line[1]))
      flightAltitude = max(flightAltitude, float(line[2]))
    else:
      g.writeline('%s %f %f' % (flightHistID, flightSpeed, flightAltitude))
      flightHistID = line[0]
      flightSpeed = float(line[1])
      flightAltitude = float(line[2])
  g.writeline('%s %f %f' % (flightHistID, flightSpeed, flightAltitude)) 
  f.close()
  g.close()
