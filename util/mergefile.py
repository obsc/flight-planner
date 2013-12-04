import tempfile
import argparse

'''
    compare function for lines, converts first two components of line to
    an int that is well ordered (sorts by flight IDs and ordinals)
'''
def sorter(line):
    stuff = line.split(' ')
    return int(stuff[0]) * 1000 + int(stuff[1])

asdiposition = lambda x: int(x.split(',')[7])
asdiflightplan = lambda x: int(x.split(',')[2])
flighthistory = lambda x:int(x.split(',')[0])
comp = asdiflightplan
timesMerged = [0]
timesMergedUp = [0]

def filesort(infile, outfile, chunkSize, mergeSize):
    files = [[]]
    print 'filesort'
    with open(infile) as f:
        f.readline() #first line just names columns
        reachedEnd = False
        while not reachedEnd:
            acc = f.readlines(chunkSize)
            if len(acc) == 0:
                reachedEnd = True
            else:
                acc.sort(key = comp)
                temp = (tempfile.TemporaryFile()).file
                temp.writelines(acc)
                temp.flush()
                files[0].append(temp)
                mergeUp(files, mergeSize)
    g = open(outfile, 'w')
    merge([elt for sl in files for elt in sl], g) #flatten, then final merge
    g.close()
    print(str(timesMerged[0]))
    print(str(timesMergedUp[0]))

'''
    merges all the files in 'files' and then puts their result in outfile
    closes each file in files, so temp files get deleted
'''
def merge(files, outfile):
    timesMerged[0] += 1
    acc = [] #initially holds the head of each file
    for f in files:
        f.seek(0)
        acc.append(f.readline())
    'return the minimum of the head positions of all files'
    def getMin():
        minElt = None
        minVal = float('inf')
        minIndex = -1
        for i in range(0, len(acc)):
            if acc[i] != "":  #make sure end of file not reached
                curVal = comp(acc[i])
                if curVal < minVal:
                    minVal = curVal
                    minElt = acc[i]
                    minIndex = i
                else:
                    pass
            else:
                pass #end of file
        acc[minIndex] = files[minIndex].readline() #replace the head of the file
        return minElt
    newf = outfile
    newline = getMin()
    while newline != None:
        newf.write(newline)
        newline = getMin()
    for f in files:
        f.close()

def merge2(file1, file2, outfile):
    file1.seek(0)
    file2.seek(0)
    head1 = file1.readline()
    head2 = file2.readline()
    while head1 != "" and head2 != "":
        if comp(head1) < comp(head2):
            outfile.write(head1)
            head1 = file1.readline()
        else:
            outfile.write(head2)
            head2 = file2.readline()
    while head1 != "":
        outfile.write(head1)
        head1 = file1.readline()
    while head2 != "":
        outfile.write(head2)
        head2 = file2.readline()
    file1.close()
    file2.close()

'''
    merges all files up to maintain the invariant below
    uses in a sense, the base [mergeSize] number representation, in such that
    each filesList[i] has len no more than mergeSize, and 
    len(filesList[i][j]) = mergeSize * len(filesList[i][j-1])
'''
def mergeUp(filesList, mergeSize):
    timesMergedUp[0] += 1
    for i in range(0, len(filesList)):
        if len(filesList[i]) >= mergeSize:
            newf = tempfile.TemporaryFile().file
            merge(filesList[i], newf)
            filesList[i] = []
            if i < len(filesList) - 1:
                filesList[i+1].append(newf)
            else:
                filesList.append([newf]) 
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'sort large files')
    parser.add_argument('infile')
    parser.add_argument('outfile')
    parser.add_argument('chunkSize', type = int)
    parser.add_argument('mergeSize', type = int)
    args = parser.parse_args()
    filesort(args.infile, args.outfile, args.chunkSize, args.mergeSize)