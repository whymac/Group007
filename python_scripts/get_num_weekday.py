#!/usr/bin/env python
import sys
import numpy, time

def parseInput(filename):
    # parse data from trip_fare_join data, which excludes head line of the columns
    fp = open(filename)
    data = fp.read().strip().split('\n')
    date = []
    for line in data:
        date.append(line.split('\t')[0])
        #num, revenue = value.split(',')
    fp.close()
    return date

def wday(date):
    if date[5:10] in holiday_list:
        return 'weekends&holidays'
    else:
        try:
            pickup_time = time.strptime(date, '%Y-%m-%d')
            pick_day = pickup_time.tm_wday
            if pick_day in (5,6):
                return 'weekends&holidays'
            else:
                return 'weekdays'
        except ValueError:
            return 'NA'

def main():
    global holiday_list
    stat = {'weekdays':0,'weekends&holidays':0}
    holiday_list = ['01-01','01-21','02-12','02-18','05-27','07-04','09-02','10-14','11-05','11-11','11-28','11-29','12-24','12-25']
    filename = sys.argv[1]
    for date in parseInput(filename):
        if wday(date) == 'weekdays':
            stat['weekdays'] = stat.get('weekdays') + 1
        else:
            stat['weekends&holidays'] = stat.get('weekends&holidays') + 1
    for item in stat.iteritems():
        print '%s\t%s' % (item[0],item[1])
                
if __name__=='__main__':
    main()
