

def splitVectors(infile, baseoutfileNoExtension):
  f = open(infile)
  line = f.readline()
  airport = line.strip().split(',')[8]
  g = open('%s%s.csv'%(baseoutfileNoExtension,airport),'w')
  g.write('FlightHistoryID,Time,Latitude,Longitude,Angle,Bearing,NextLat,NextLon,Airport,Altitude,Speed\n')
  g.write(line)
  for line in f:
    new_airport = line.strip().split(',')[8]
    if new_airport == airport:
      g.write(line)
    else:
      g.close()
      airport = new_airport
      g = open('%s%s.csv'%(baseoutfileNoExtension,airport),'w')
      g.write('FlightHistoryID,Time,Latitude,Longitude,Angle,Bearing,NextLat,NextLon,Airport,Altitude,Speed\n')
      g.write(line)
  g.close()
  f.close()