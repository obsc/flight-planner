Flight-planner
paper 36
Alex Guziel-asg252, Atheendra PT-ap778, Bo Zhou-bz88, Rene Zhang-rz99
We ran this with Python 2.7 on Windows 7 x64. 

Our library dependencies are SciKit-Learn, Shapely, Pandas, and GeoPy. We also use some open-source code provided by a competition admin.

We start with folder basicAgent
This uses a modified version of some open source but most of it has been gutted significantly. To run this, just do python basicAgent.py. You need to have the file called restrictedZones.csv and TestFlights.csv in the same folder as well which can be downloaded from the Kaggle site.

For util, there is a lot of utilities here.
In alphabetical order:
astar.py:
This is just a module that is imported.

distance.py
This just is a file that is imported.

extract.py
relevant:
extract(indexList, infile, outfile, chunk)
This will take infile (a csv file) and return a file with the columns in indexList printed to outfile. Chunk determines the ratio of lines to include (chunk =1 is all lines, chunk=2 is one half)

accumulate(infileList, idIndexList, indexListList, outfile)
infileList is a list of files, idIndexList is which flightIds to look for, and indexListList is list of columns we want in each file, and outfile is the output file, we use this to merge files together)

fileutil.py
convertIndex(infile, outfile)
infile is the filename of a file in the format of asdiflightplan, and maps the IDs in there to flight hist IDs in a new file. Useful because data has inconsistent ID labeling.

getMaxCruise(infile, outfile)
For each flightID, prints the max altitiude and speed for each flight ID.

greatcircle.py
A utility file for producing shortest paths along a sphere, which has a more involved calculation than Cartesian coordinates if we want to segment a path.
get_path(start, dest, n)
start and end are (latitude, longitude) tuples corresponding to points, and n is the number of chunks to split up.

to_latlon(northings, eastings, altitude)
converts lambert conformal conic projection to latitude and longitude

get_dist(start, dest)
start and dest are latitude longitude tuples, and returns distance

learner.py
call python learner.py, need the file 'dat/filtered.csv' and 'dat/training2_speedalt' to exist which come from running other files. Runs models to classify cruise speed and altitude onto a path.

map.py
mapToMaxAltSpeed
need to have the data in the directories
'../allData/ttrain/training2_asdipostion.csv' and then returns max alt speed mapped from flight history (this is redundant function)

mapToPercentileSpeed
returns a percentile based mapping of speed

mapToDistance
need to have '../data/GEKaggle/TTrain/training2_flighthistory.csv'
produces a map of flihgts to distances

mapPoints.py
various utilies
mapToVectors(asdipositionsorted, sortFlightHistory, airportFile, outfile)
needs to input
asdipositionsorted = training2_asdiposition.csv from training set sorted by flighthistoryid
sortedFlightHistory = flightHistory file from training set sorted by ID
airportFile = airports.csv, given in latitude and longitude
outfile = output file
produces a file vectors.csv with various labeled data correponding to information on a waypoint of a flight

mergefile.py
external merge sortfor files
comp must be changed to the name of file, we use the ones in the four lines above correposnding to the similar file name in the training/test sets
then run
python mergefile.py infile outfile chunkSize mergeSize
infile is the file to sort, outfile is the output file, chunkSize is the size to load each part in bytes(usually 1% of the file works well), mergeSize is how many chunks to merge at once (10 seems to work well)

parse.py
helps parse things, generally self documenting

path.py
run as python path.py
need ot have files 'dat/IMPORTANTHASHTAG.csv', 'dat/TestFlights.csv' and 'dat/splitBase.csv'. Basically, writes  path where splitBase is the astar path chunked into 32 chunks, and IMPORTANTHASHTAG is the astar paths not split up

renerunthis.py
getPaths(outfile) writes a pickled dict to the outfile for each airport to airport path. Unused.

sim.py
Some similarity measures we tried for KNN that did not work out well because they are not true metrics.

smooth.py 
howunsmooth(filename)
gives a submission file and sees how many penalties we get for altitude changes, only for reference

smoothaltitude(altitudeList)
takes in a list of altitudes, and does a smoothing routine that works poorly)

naiveSmoothing(altitudeList)
makes the altitudes conform better  so the flight has two stages, ascent and descent, or maybe just descent. Very sensitive to outliers

split.py
python split.py -s s -e e -d d -o o input size
s is the starting line position 
e is the ending line postion
d is output directory
o is stem for output files
input is filename
size is number of lines for each chunk

splitVectors.py
first we use splitVectors(infile, baseoutfileNoExtension)
where we give the infile which is produced by the file in other thing vectors which given a list of arguments, is kind of dependent, and the extension to call the output.
produceFeatures takes the files from there, and produces relevant features of it

produceAugmentedFeatures uses more features

produceVectors takes in the testFlights file, the submission file, the vectorFileBase (a name we  choose) the airports file, and the file to write the submission to. Classifies the points in submission by using the data in testFlights and creates model from vectorFileBase.

vectorProduction(testFlights, submission, vectorFileBase, outsubmissionbased)
testflights is testflights.csv, submission is the submission wed like to modify
vectorfilebase is what we call the vector file from producefeatures, and outsubmissionbased is where we output the model
trains a few airports at a time so we dont run out of ram.


