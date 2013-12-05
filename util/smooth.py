

def howunsmooth(filename):
  with open(filename) as f:
    f.readline()
    firstline = f.readline()
    stuff = firstline.strip().split(',')
    curFHID = int(stuff[0])
    lastAlt = int(stuff[4])
    areIncreasing = True
    curFlipCount = 0
    totalFlipCount = 0
    for line in f:
      stuff = line.strip().split(',')
      if int(stuff[0]) == curFHID:
        if areIncreasing:
          if int(stuff[4]) >= lastAlt:
            pass
          else:
            curFlipCount += 1
            areIncreasing = False
        else:
          if int(stuff[4]) <= lastAlt:
            pass
          else:
            curFlipCount += 1
            areIncreasing = True
        lastAlt = int(stuff[4])
      else:
        curFlipCount = (curFlipCount-5) if (curFlipCount-5) >= 0 else 0
        totalFlipCount += curFlipCount
        curFlipCount = 0
        curFHID = int(stuff[0])
        lastAlt = int(stuff[4])
        areIncreasing = True
  print str(totalFlipCount)

def smoothaltitude(altitudeList):
  while countFlips(altitudeList) > 5:
    trough = altitudeList[0]
    trough_i = 0
    peak_i = 0
    peak = altitudeList[0]
    shittiest_change = 0.0
    shittiest_indices = (0,0)
    areIncreasing = True
    old_altitude = altitudeList[0]
    for ii in range(0, len(altitudeList)):
      if areIncreasing:
        if altitudeList[ii] < old_altitude:
          change = max(float(peak)-altitudeList[ii],altitudeList[ii]-float(peak))
          if change >shittiest_change:
            shittiest_change = change
            shittiest_indices = (peak_i,ii)
          else:
            pass
          peak_i = ii
          peak = altitudeList[ii]
          areIncreasing = True
        else:
          pass
      else:
        if altitudeList[ii] > old_altitude:
          change = max(float(trough)-altitudeList[ii],altitudeList[ii]-float(trough))
          if change > shittiest_change:
            shittiest_change = change
            shittiest_indices = (trough_i,ii)
          else:
            pass
          trough_i = ii
          trough = altitudeList[ii]
          areIncreasing = False
        else:
          pass
      old_altitude = altitudeList[ii]
    start_i, end_i = shittiest_indices
    diff = float(altitudeList[end_i]) - float(altitudeList[start_i])
    for jj in range(start_i, end_i+1):
      alt = (jj-start_i) * diff
      altitudeList[jj] = alt
  return altitudeList

def naiveSmoothing(altitudeList):
  startAltitude = altitudeList[0]
  minAltitude = altitudeList[0]
  maxAltitude = altitudeList[0]
  for altitude in altitudeList:
    minAltitude = min(altitude,minAltitude)
    maxAltitude = max(altitude,maxAltitude)
  hitMax = True if maxAltitude == startAltitude else False
  lastAlt = altitudeList[0]
  for ii in range(1, len(altitudeList)):
    if altitudeList[ii] >= maxAltitude:
      hitMax = True
    else:
      if hitMax:
        if altitudeList[ii] > lastAlt:
          altitudeList[ii] = lastAlt
        else:
          pass 
      else:
        if altitudeList[ii] < lastAlt:
          altitudeList[ii] = lastAlt
        else:
          pass
    lastAlt = altitudeList[ii]
  return altitudeList




def countFlips(altitudeList):
  areIncreasing = True
  flipCount = 0
  old_altitude = altitudeList[0]
  for altitude in altitudeList:
    if areIncreasing:
      if altitude >= old_altitude:
        pass
      else:
        flipCount += 1
        areIncreasing = False
    else:
      if altitude <= old_altitude:
        pass
      else:
        flipCount += 1
        areIncreasing = True
    old_altitude = altitude
  return flipCount