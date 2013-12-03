'''
  given int list of 0-based indices of which columns, returns new csv
  with the attributes labeled at the top
'''
def extract(indexList, infile, outfile):
  f = open(infile)
  g = open(outfile,'w')
  temp = line.split(f.readline())
  for index in indexList:
    str_build += temp[indexList] + ','
  str_build = str_build[0:len(str_build)-1] + '\n'
  g.write(str_build)
  for line in infile:
    str_build = ''
    temp = line.split(',')
    for index in indexList:
      str_build += temp[indexList] + ','
    str_build  = str_build[0:len(str_build)-1] + '\n'
    g.write(str_build)
  f.close()
  g.close()
