# -*- coding: utf-8 -*-
"""
Created on Wed Dec 04 18:34:11 2013

@author: Atheendra
"""

from lshash import LSHash

global_training_route = [ ]
next_hop_index = -1

#  Processed_Routes_file has fields flight_id, LAT, LONG,
#                                   DELAY_COST, TIME_OF_TRAVEL,
#                                   DESTINATION, 
#                                   NEXT_HOP
def get_training_routes(processed_routes_file):
    training_set = []
    infile = open(processed_routes_file)
    infile.readline()
    for line in infile:
        splitter = line.rstrip().split(',')
        new_entry = []
        for i in range(1, len(splitter)):
            new_entry.append(splitter[i])
        training_set.append(new_entry)
    infile.close()
    return training_set

def learn(routes):
    global global_training_route
    global next_hop_index
    
    extra_data_len = 2    #destination, next_hop
    ndims = len(routes[0]) - extra_data_len   #Number of dimensions
    hash_length = len(routes[0]) * 2   #arbitrarily chosen hash_length
    next_hop_index = len(routes[0]) - 1   #NextHop index at the last
    
    for i in range(0, len(routes) - 1):
        if(routes[i][next_hop_index] >= routes[i+1][next_hop_index]):
            routes[i][next_hop_index] = i+1
        else:
            routes[i][next_hop_index] = -1
    global_training_route = routes
    lsh = LSHash(hash_length, ndims)
    for entry in routes:
        lsh.index(entry[:-extra_data_len], extra_data = entry[-extra_data_len:])
    return lsh
    
def read_test_flight(test_flight_path):
    infile = open(test_flight_path)
    infile.readline()
    test_input = []
    for line in infile:
        splitter = line.rstrip().split(',')
        entry = []
        entry.append(splitter[0]) #0 = FlightHistoryId
        entry.append(splitter[2]) #1 = destination
        entry.append(splitter[3]) #2 = Travel time
        entry.append(splitter[4]) #3 = Latitude
        entry.append(splitter[5]) #4 = Longitude
        entry.append(splitter[6]) #5 = Altitude
        entry.append(splitter[7]) #6 = GroundSpeed
        test_input.append(entry)
        break
    infile.close()
    return test_input

def follow_path(route):
    return_path = []
    return_path.append([route[0][0], route[0][1]]) #Latitude, long
    next_index = route[0][2]
    while next_index != -1:
        return_path.append([global_training_route[next_index][0], 
                             global_training_route[next_index][1]])
        next_index = global_training_route[next_index][next_hop_index]
        
    return return_path

def construct_output(learned_hash, test_inp):
    outfile = open("knnSubmission.csv", "w")
    outfile.write("FlightId,Ordinal,LatitudeDegrees,LongitudeDegrees,AltitudeFeet" + \
                   "AirspeedKnots\n")
    for i in test_inp:
        spatiality = [i[3], i[4], 0, i[2]]
        current_speed = i[6]
        current_altitude = i[5]
        destination = i[1]
        
        result = learned_hash.query(spatiality)[:10]
        path = []
        for r in result:
            if r[0][1] == destination:
                path = follow_path(r)
        if(len(path) == 0):
            print "That destination wasn't in the training set"
        else:
            for ordinal, point in enumerate(path):
                outfile.write(i[0]) #FlightId
                outfile.write(",")
                
                outfile.write(ordinal)
                outfile.write(",")
                
                outfile.write(point[0]) #Lat
                outfile.write(",")
                
                outfile.write(point[1]) #Long
                outfile.write(",")
                
                outfile.write(current_altitude)
                outfile.write(",")
                
                outfile.write("450\n") #Maintain constant airspeed
    outfile.close()
        

def main(routes_file_path, test_flight_path):
    routes = get_training_routes(routes_file_path)
    learned_hash = learn(routes)
    test_input = read_test_flight(test_flight_path)
    construct_output(learned_hash, test_input)
    

if __name__ == "__main__":
    main("E:\\TrainingRoute.csv", 
             "D:\\Cornell\\4780ML\\flight\\flight-planner\\basicAgent\\TestFlights.csv")
    
    '''if(len(args)>1):
        main(args[1], args[2])
    else:
        
        
lsh = LSHash(2, 2)
i = 0
for p in path:
    lsh.index(p, extra_data=i)
    i += 1
print lsh.query([38.2, -120])[0][0][1]'''
