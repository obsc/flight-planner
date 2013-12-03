import Distance
def mapToMaxAltSpeed():
  f= open('../data/GEKaggle/TTrain/training2_asdiposition.csv')
  f.readline()
  g = open('../data/GEKaggle/TTrain/training2_speedalt','w')
  line = f.readline()
  line = line.split(',')
  flightHistID = int(line[7])
  flightSpeed = int(line[4])
  flightAltitude = int(line[3])
  for line in f:
    lines = line.split(',')
    try:
      if int(lines[7]) == flightHistID:
        flightSpeed = max(flightSpeed, int(lines[4]))
        flightAltitude = max(flightAltitude, int(lines[3]))
      else:
        g.write('%i %i %i\n' % (flightHistID, flightSpeed, flightAltitude))
        flightHistID = int(lines[7])
        flightSpeed = int(lines[4])
        flightAltitude = int(lines[3])
    except ValueError:
      print line
  g.write('%i %i %i\n' % (flightHistID, flightSpeed, flightAltitude)) 
  f.close()
  g.close()

def mapToDistance():
  f = open('../data/GEKaggle/TTrain/training2_flighthistory.csv')
  f.readline()
  g = open('../data/GEKaggle/TTrain/training2_distance','w')
  count = 0
  for line in f:
    try:
      lines = line.split(',')
      flightHistID = int(lines[0])
      start = lines[5] 
      end = lines[7]
      distance = Distance.airportDistance(start, end)
      g.write('%i %f %s %s\n' % (flightHistID, distance, start, end))
    except ValueError:
      count += 1
    except Distance.InvalidAirport:
      count += 1
  print str(count)
  g.close()
  f.close()


