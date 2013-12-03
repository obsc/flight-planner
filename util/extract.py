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

"""
Accumulates the data in every file in infileList and creates a new file outfile
containing all of the information
"""
def accumulate(infileList, outfile):

  # Find all of the ids in the files and sort
  idList = []
  for filename in infileList:
    f = open(filename)
    for line in f: 
      idList.append(int(line.split(',')[0]))
    f.close()
  idList.sort()
  idSet = list(set(idList))

  out = open(outfile, 'r+')
  # Open files one at a time
  for i in range(0,len(infileList)):
    out.seek(0)
    f = open(infileList[i])
    # uncomment if first line is text
    #f.readline()
    str_build = ""
    j = 0

    # We go through all of the ids
    while j < len(idSet):
      write_back = out.tell()
      if i == 0:
        str_build += str(idSet[j]) + ','
      else:
        str_build += out.readline().rstrip('\n') + ','
      last_pos = f.tell()
      lines = f.readline().split(',')
      # If id doesn't match up, append empty
      if int(lines[0]) != idSet[j]: 
        for index in range(1,(len(lines))): 
          if index == len(lines) - 1:
            str_build += '\n'
            f.seek(last_pos)
          else:
            str_build += ','
      # Otherwise, append the information
      else: 
        for index in range(1,(len(lines))): 
          if index == len(lines) - 1:
            str_build += lines[index]
          else:
            str_build += lines[index] + ','
      j +=1
    f.close()
    # Rewrite the file with the new contents
    out.seek(0)
    out.truncate()
    out.write(str_build)
  out.close()

  """
  for i in set(idList):
    
    ''' concatenate all of the file lines for an id '''
    for j in len(outfileList):
      f = open(outfile+"part"+str(j))
      ''' Mark the place in file in case id doesn't match '''
      last_pos = f.tell()
      line = f.readline()
      line = line.split(',')
      
      if int(line[0]) == i:
        for index in (len(line) - 1): 
          str_build += line[index+1] + ','
      ''' Else we append empty and move back'''
      else: 
        for index in (len(line) - 1): 
          str_build += ','
          f.seek(last_pos)
    str_build += '\n'
    """
  

  