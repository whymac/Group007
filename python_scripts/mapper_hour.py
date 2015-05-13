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

def wday(date):
    if date[5:10] in holiday_list:
        return 'weekends&holidays'
    else:
        try:
            pickup_time = time.strptime(date, '%Y-%m-%d %H:%M:%S')
            pick_day = pickup_time.tm_wday
            if pick_day in (5,6):
                return 'weekends&holidays'
            else:
                return 'weekdays'
        except ValueError:
            return 'NA'

def mapper():
    global holiday_list
    holiday_list = ['01-01','01-21','02-12','02-18','05-27','07-04','09-02','10-14','11-05','11-11','11-28','11-29','12-24','12-25']
    for values in parseInput():
        if values[10] and values[11] and values[12] and values[13]:
            print '%s,%s\t%d,%.2f,%.2f' % (wday(values[3]),values[3][11:13],1,float(values[-1]),float(values[-3]))
                
if __name__=='__main__':
    mapper()
