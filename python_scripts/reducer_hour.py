#!/usr/bin/python

import sys

current_key = None
current_value1 = 0
current_value2 = 0
current_value3 = 0

# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    
    key, value= line.strip('\n').split('\t')
    value1, value2, value3 = value.split(',')
    
    try:
        value1 = int(value1)
        value2 = float(value2)
        value3 = float(value3)

    except ValueError:
        continue
    
    if key == current_key:
        current_value1 += value1
        current_value2 += value2
        current_value3 += value3
    else:
        if current_key:
            print "%s\t%d,%.2f,%.2f" % (current_key, current_value1, current_value2, current_value3)
        current_key = key
        current_value1 = value1
        current_value2 = value2
        current_value3 = value3

# output goes to STDOUT (stream data that the program writes)
print "%s\t%d,%.2f,%.2f" % (current_key, current_value1, current_value2, current_value3)