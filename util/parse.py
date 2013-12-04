import csv
import greatcircle

F = csv.reader(open("dat/AirportsLatLong.csv"))
F.next()
LOC = {}
for row in F:
  LOC[row[0]] = (float(row[1]), float(row[2]))

""" Initializes file by clearing """
def init_file(f):
  open(f,'w').close()

""" Writes to output file """
def write_file(outfile, out):
  writer = csv.writer(open(outfile,'w'), lineterminator='\n')
  writer.writerows(out)

""" Converts time """
def convert_time(time):
  time = time.strip().split(" ")[1]
  time = time.split("+")[0]
  time = time.split(":")
  t = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
  return t

def get_location(loc):
  if len(loc) == 3:
    loc = "K" + loc
  return LOC[loc]

""" Fixes a single row to have the correct features """
def fix_row(row):
  (startx, starty) = get_location(row[1])
  (endx, endy) = get_location(row[2])
  dist = greatcircle.get_dist((startx, starty), (endx, endy))
  dtime = convert_time(row[3])
  edtime = convert_time(row[4])
  eatime = convert_time(row[5])

  return [str(x) for x in [row[0], startx, starty, endx, endy, dist, dtime, edtime, eatime]]

""" Parses all the rows """
def parse(infile, outfile):
  f = csv.reader(open(infile))
  out = []
  prev = None

  for row in f:
    if prev is not None and row[0] != prev[0]:
      try:
        out.append(fix_row(prev))
      except:
        pass
    prev = row
  try:
    out.append(fix_row(prev))
  except:
    pass

  write_file(outfile, out)