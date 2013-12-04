from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib
import csv

def get_labels(f):
  f = open(f)
  spds = {}
  alts = {}
  for line in f:
    line = line.strip().split(" ")
    spds[line[0]] = float(line[1])
    alts[line[0]] = float(line[2])
  f.close()
  return (spds, alts)

def main(features, speedalt):
  (spds,alts) = get_labels(speedalt)
  f = csv.reader(open(features))
  X = []
  S = []
  A = []

  for row in f:
    if row[0] in spds:
      X.append([float(x) for x in row[1:]])
      S.append(spds[row[0]])
      A.append(alts[row[0]])

  clf = RandomForestRegressor(n_estimators = 10)

  print "Calculating Speed Model"
  spd = clf.fit(X,S)
  joblib.dump(spd, "RandomForest/spd")
  print "Calculating Altitude Model"
  alt = clf.fit(X,A)
  joblib.dump(alt, "RandomForest/alt")

def apply(featurefile, infile, outfile, spd, alt):
  spd = joblib.load(spd)
  alt = joblib.load(alt)

  features = {}
  f = csv.reader(open(featurefile))
  for row in f:
    features[row[0]] = [float(a) for a in row[1:]]

  out = []
  f = csv.reader(open(infile))

  for row in f:
    if row[0] in features:
      if row[4] == "38000":
        row[4] = str(int(alt.predict(features[row[0]])[0]))
      row[5] = str(int(spd.predict(features[row[0]])[0]))
    out.append(row)

  writer = csv.writer(open(outfile,'w'), lineterminator='\n')
  writer.writerows(out)

if __name__ == "__main__":
  main("dat/filtered.csv", "dat/training2_speedalt")