from sklearn.ensemble import RandomForestRegressor
from sklearn.externals import joblib
import csv

def get_speeds(f):
  f = open(f)
  spds = {}
  for line in f:
    line = line.strip().split(" ")
    spds[line[0]] = float(line[1])
  f.close()
  return spds

def main(features, speedalt):
  spds = get_speeds(speedalt)
  f = csv.reader(open(features))
  X = []
  Y = []

  for row in f:
    if row[0] in spds:
      X.append([float(x) for x in row[1:]])
      Y.append(spds[row[0]])

  clf = RandomForestRegressor(n_estimators = 10)
  model = clf.fit(X,Y)
  joblib.dump(model, "model/model")

if __name__ == "__main__":
  main("dat/filtered.csv", "dat/training2_speedalt")