#!/usr/bin/python

import sys
import string 

current_key = None
current_value = None
trips = []
fares = []

# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    
    key, value = line.strip().split("\t", 1)


    if key == current_key:        
        if len(current_value.split(',',)) == 10:
            trips.append(current_value)
        if len(current_value.split(',',)) == 7:
            fares.append(current_value)
    else:
        if current_key:
            if len(current_value.split(',',)) == 10:
                trips.append(current_value)
            if len(current_value.split(',',)) == 7:
                fares.append(current_value)
            for i in range(0,len(trips)):
                for j in range(0,len(fares)):
                    print "%s\t%s,%s" %(current_key, trips[i],fares[j])
            trips = []
            fares = []

            
        current_key = key
    current_value = value

    
        
# output goes to STDOUT (stream data that the program writes)
if len(current_value.split(',',)) == 10:
    trips.append(current_value)
if len(current_value.split(',',)) == 7:
    fares.append(current_value)
for i in range(0,len(trips)):
    for j in range(0,len(fares)):
        print "%s\t%s,%s" %(current_key, trips[i],fares[j])