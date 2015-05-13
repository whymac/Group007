#!/usr/bin/env python
import sys
import numpy, time
import os

def parsedir(dirname):
    # parse data
    if not os.path.exists('.'+os.sep+'popular_trips'):
        os.mkdir('.'+os.sep+'popular_trips')
    f = open('.'+os.sep+'popular_trips'+os.sep+'popular_trips.csv' , 'w')
    line = '{},{},{},{},{},{}\n'.format('source','destination','time of trips','revenue','tip amount','tip percentage') 
    f.write(line)
    trips = {}
    for files in os.walk('.'+os.sep+dirname):
        for filename in files[2]:
            if filename[:4] == '2013':
                fp = open('.'+os.sep+dirname+os.sep+filename)
                data = fp.read().strip().split('\n')
                for line in data:
                    key, value = line.split('\t')
                    time_of_trips, total_revenue, tip_amout = value.split(',')
                    try:
                        time_of_trips = int(time_of_trips)
                        total_revenue = float(total_revenue)
                        tip_amout = float(tip_amout)
                    except ValueError:
                        continue
                    time_of_trips = trips.get(key, [0,0,0,0])[0] + time_of_trips
                    total_revenue = trips.get(key, [0,0,0,0])[1] + total_revenue
                    tip_amout = trips.get(key, [0,0,0,0])[2] + tip_amout
                    trips[key] = [time_of_trips, float(total_revenue), float(tip_amout), float(round(tip_amout/total_revenue,4))]
                fp.close()
    for key, value in sorted(trips.items(), key=lambda (k,v):(v,k),reverse = True):
        source = key.split(',')[0]
        destination = key.split(',')[1]       
        line = '{},{},{},{},{},{}\n'.format(source,destination,value[0],value[1],value[2],value[3]) 
        f.write(line)
    f.close()

def main():
    dirname = sys.argv[1]
    parsedir(dirname)
                
if __name__=='__main__':
    main()
