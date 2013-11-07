import os
from optparse import OptionParser

def parse(fileName, s, e, size):
    """ Generator returning file chunks from main file """
    with open(fileName) as f:
        lineNum = 0
        outSize = 0
        out = ""
        for line in f:
            lineNum += 1
            if lineNum < s:
                continue
            if e != -1 and lineNum > e:
                break
            
            outSize += 1
            out += line
            if outSize == size:
                yield (out, outSize)
                outSize = 0
                out = ""
        if out:
            yield (out, outSize)

def writeFiles(opts, args):
    """ Writes to new files """
    try:
        os.mkdir(opts.dir)
    except OSError:
        pass #Directory exists

    outFile = os.path.join(opts.dir, opts.out) + "%s"
    num = 0
    start = opts.start
    for (s, n) in parse(args[0], opts.start, opts.end, int(args[1])):
        if opts.verbose:
            print "Writing lines %s-%s to file: %s" % (start,
                    start + n - 1, outFile % num)
        f = open(outFile % num, 'w')
        f.write(s)
        f.close()

        num += 1
        start += n

def main():
    """ Parses command line arguments """
    usage = "usage: %prog [options] input size"
    parser = OptionParser(usage)
    parser.add_option("-s", type="int", dest="start",
                        default=1, help="starting line")
    parser.add_option("-e", type="int", dest="end",
                        default=-1, help="ending line")
    parser.add_option("-d", dest="dir", default="out",
                        help="output file directory")
    parser.add_option("-o", dest="out", default="out",
                        help="output file stem")
    parser.add_option("-v", action="store_true", dest="verbose",
                        default=True, help="verbose mode")
    parser.add_option("-q", action="store_false", dest="verbose",
                        help="quiet mode")
    (opts, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("invalid number of arguments")

    return (opts, args)

if __name__ == "__main__":
    (opts, args) = main()
    writeFiles(opts, args)