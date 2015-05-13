#!/usr/bin/env python
import sys
import numpy, time
import os

def parsedir(dirname):
    # parse data
    if not os.path.exists('.'+os.sep+'total trips each hour'):
        os.mkdir('.'+os.sep+'total trips each hour')
    f = open('.'+os.sep+'total trips each hour'+os.sep+'total trips each hour.csv' , 'w')
    line = '{},{},{}\n'.format('hour','weekdays','weekends&holidays') 
    f.write(line)
    weekdaypair = {}
    weekendpair = {}
    for files in os.walk('.'+os.sep+dirname):
        for filename in files[2]:
            if filename[-3:] == 'day':
                fp = open('.'+os.sep+dirname+os.sep+filename)
                data = fp.read().strip().split('\n')
                for line in data:
                    key, value = line.split('\t')
                    hour = key.split(',')[1]
                    num = value.split(',')[0]
                    try:
                        num = int(num)
                    except ValueError:
                        continue
                    if key.split(',')[0] == 'weekdays':
                        weekdaypair[hour] = weekdaypair.get(hour,0) + num
                    else:
                        weekendpair[hour] = weekendpair.get(hour,0) + num
                fp.close()
    for h in sorted(weekdaypair.keys()):
        line = '{},{},{}\n'.format(h,weekdaypair[h]/247,weekendpair[h]/118)   
        f.write(line)
    f.close()

def main():
    dirname = sys.argv[1]
    parsedir(dirname)
                
if __name__=='__main__':
    main()
