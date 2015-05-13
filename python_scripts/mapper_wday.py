#!/usr/bin/env python
import sys
import numpy, time

def parseInput():
    # parse data from trip_fare_join data, which excludes head line of the columns
    for line in sys.stdin:
        line = line.strip('\n')
        part1, part2 = line.split('\t')
        values = part1.split(',')
        values.extend(part2.split(','))
        yield values

def mapper():
    for values in parseInput():
        if values[10] and values[11] and values[12] and values[13]:
            print '%s\t%d,%.2f,%.2f' % (values[3][:10],1,float(values[-1]),float(values[-3]))
                
if __name__=='__main__':
    mapper()
