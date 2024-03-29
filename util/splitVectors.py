import mapPoints
import sklearn.ensemble as ske
import sklearn.neighbors as skn
import distance
import sim
import smooth

def newModel():
  #model = ske.ExtraTreesRegressor()
  model = ske.GradientBoostingRegressor()
  #model = skn.KNeighborsRegressor(n_neighbors=10,weights='distance',algorithm='auto')
  return model

def vectorProduction(testFlights, submission, vectorFileBase, outsubmissionbased):
  airports = ['KPSP','KCID','KCOS','KFAT','KXNA','KLIT','KTUS','KDSM','KTUL','KPBI','KELP','KRSW','KLGB','KBUR','KOKC','KONT','KDAL','KABQ','KCMH','KMKE','KRDU','KMSY','KSMF','KSDF','KSJC','KSNA','KCVG','KIND','KTPA','KCLE','KOAK','KBNA','KHOU','KMCI','KSTL','KFLL','KMIA','KMEM','KBWI','KPDX','KSAN','KDCA','KIAD','KMCO','KMDW','KLGA','KSLC','KPHL','KPHL','KBOS','KCLT','KDTW','KEWR','KJFK','KSEA','KMSP','KIAH','KPHX','KSFO','KDEN','KDFW','KATL','KLAX','KORD']
  indices = [0,10,20,30,35,40,45,48,50,52,53,54,55,56,57,58,59,60,61,62,63,64]
  curIndex = 0
  curSubmission = submission
  writeSubmission = ('%s%i.csv') % (outsubmissionbased,curIndex)
  for i in range(0, len(indices)-1):
    start = indices[i]
    end = indices[i+1]
    produceVectors(testFlights,curSubmission,vectorFileBase,airports[start:end],writeSubmission)
    curSubmission = writeSubmission
    curIndex += 1
    writeSubmission = ('%s%i.csv') % (outsubmissionbased,curIndex)

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

def produceFeatures(splitVectorFile):
  features= []
  targets = []
  with open(splitVectorFile) as f:
    f.readline()
    for line in f:
      stuff = line.strip().split(',')
      feature = [float(stuff[2]),float(stuff[3]),float(stuff[5])]
      target = int(stuff[9])
      features.append(feature)
      targets.append(target)
  return (features, targets)

def produceAugmentedFeatures(splitVectorFile):
  features = []
  targets = []
  with open(splitVectorFile) as f:
    f.readline()
    for line in f:
      stuff = line.strip().split(',')
      feature = [float(stuff[2]),float(stuff[3]),float(stuff[5]),float(stuff[9])]
      target = int(stuff[10])
      features.append(feature)
      targets.append(target)
  return (features,targets)



def produceVectors(testFlights, submission, vectorFileBase, airports, outsubmission):
  dictWithFlights = dict()

  with open(testFlights) as f:
    f.readline()
    for line in f:
      stuff = line.strip().split(',')
      airport = stuff[2]
      flightID = int(stuff[0])
      dictWithFlights[flightID] = airport
  flightList = []
  with open(submission) as f:
    f.readline()
    firstline = f.readline()
    curAcc = []
    curFHID = int(firstline.strip().split(',')[0])
    curAcc.append(firstline)
    for line in f:
      stuff = line.strip().split(',')
      if int(stuff[0]) == curFHID:
        curAcc.append(line)
      else:
        flightList.append(curAcc)
        curFHID = int(stuff[0])
        curAcc = [line]
    flightList.append(curAcc)
  modelDict = dict()
  for airport in airports:
    filename = '%s%s.csv'%(vectorFileBase,airport)
    features, targets = produceFeatures(filename)
    model1 = newModel()
    model1.fit(features,targets)
    afeatures, atargets = produceAugmentedFeatures(filename)
    model2 = newModel()
    model2.fit(afeatures,atargets)
    modelDict[airport] = (model1, model2)

  f = open(outsubmission,'w')
  f.write('FlightId,Ordinal,Latitude,Longitude,Altitude,AirSpeed\n')
  for flight in flightList:
    airport = dictWithFlights[int(flight[0].strip().split(',')[0])]
    if airport in modelDict:

      altitudeList = []
      for ii in range(0, len(flight)-1):
        curLine = flight[ii].strip().split(',')
        nextLine = flight[ii+1].strip().split(',')
        lat1,lon1 = (float(curLine[2]),float(curLine[3]))
        lat2,lon2 = (float(nextLine[2]),float(nextLine[3]))
        bearing = mapPoints.calcBearing(lat1,lon1,lat2,lon2)
        model1,model2 = modelDict[airport]
        feature = [lat1,lon1,bearing]
        altitude = int(model1.predict(feature))
        altitudeList.append(altitude)
      curLine = flight[len(flight)-1].strip().split(',')
      lat1,lon1 = (float(curLine[2]),float(curLine[3]))
      lat2,lon2 = distance.airportToLatLon(airport)
      bearing = mapPoints.calcBearing(lat1,lon1,lat2,lon2)
      model1,model2 = modelDict[airport]
      feature = [lat1,lon1,bearing]
      altitude = int(model1.predict(feature))
      altitudeList.append(altitude)
      smooth.naiveSmoothing(altitudeList)
      for ii in range(0, len(flight)-1):
        curLine = flight[ii].strip().split(',')
        nextLine = flight[ii+1].strip().split(',')
        lat1,lon1 = (float(curLine[2]),float(curLine[3]))
        lat2,lon2 = (float(nextLine[2]),float(nextLine[3]))
        bearing = mapPoints.calcBearing(lat1,lon1,lat2,lon2)
        model1,model2 = modelDict[airport]
        feature = [lat1,lon1,bearing,altitudeList[ii]]
        speed = int(model2.predict(feature))
        newCurLine = '%s,%s,%f,%f,%i,%i\n' % (curLine[0], curLine[1], lat1, lon1, altitudeList[ii], speed)
        f.write(newCurLine)
      curLine = flight[len(flight)-1].strip().split(',')
      lat1,lon1 = (float(curLine[2]),float(curLine[3]))
      lat2,lon2 = distance.airportToLatLon(airport)
      bearing = mapPoints.calcBearing(lat1,lon1,lat2,lon2)
      model1,model2 = modelDict[airport]
      feature = [lat1,lon1,bearing,altitudeList[len(altitudeList)-1]]
      speed = int(model2.predict(feature))
      newCurLine = '%s,%s,%f,%f,%i,%i\n' % (curLine[0], curLine[1], lat1, lon1, altitudeList[len(altitudeList)-1], speed)
      f.write(newCurLine)

    else:
      for line in flight:
        f.write(line)
  f.close()
