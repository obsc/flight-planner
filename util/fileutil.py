

'''
    USAGE: takes in asdiflightplan and makes a file that maps
    the flightplan IDs to flighthist IDs
'''
def convertIndex(infile, outfile):
  f = open(infile)
  g = open(outfile, 'w')
  f.readline()
  for line in f:
    'take the two different ids'
    line = line.split(',')
    g.write(line[0] + ' ' + line[2] + '\n')
  f.close()
  g.close()

'''
    USAGE: take in asdiposition and print out a mapping from flighthist_id
    to max alt,speed
'''
def getMaxCruise(infile, outfile):
  f = open(infile)
  g = open(outfile, 'w')
  maxCruise = dict()
  f.readline()
  for line in f:
    try:
      line = line.split(',')
      flightHistID = int(line[7])
      altitude = int(line[3])
      speed = int(line[4])
      if flightHistID in maxCruise:
        alt, spd = maxCruise[flightHistID]
        altitude = max(altitude, alt)
        speed = max(speed,spd)
        maxCruise[flightHistID] = (altitude,speed)
      else:
        maxCruise[flightHistID] = (altitude,speed)
    finally:
      pass
  for k, v in maxCruise.iterItems():
    g.write(str(k) + ' ' + str(v) + '\n')
  f.close()
  g.close()