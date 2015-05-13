#!/usr/bin/env python
import sys
sys.path.append('.')
import matplotlib
matplotlib.use('Agg')
from matplotlib.path import Path
from rtree import index as rtree
import numpy, shapefile, time

def findNeighborhood(location, index, neighborhoods):
    match = index.intersection((location[0], location[1], location[0], location[1]))
    for a in match:
        if any(map(lambda x: x.contains_point(location), neighborhoods[a][1])):
            return a
    return -1

def readNeighborhood(shapeFilename, index, neighborhoods):
    sf = shapefile.Reader(shapeFilename)
    for sr in sf.shapeRecords():
        if sr.record[1] not in ['New York', 'Kings', 'Queens', 'Bronx']: continue
        paths = map(Path, numpy.split(sr.shape.points, sr.shape.parts[1:]))
        bbox = paths[0].get_extents()
        map(bbox.update_from_path, paths[1:])
        index.insert(len(neighborhoods), list(bbox.get_points()[0])+list(bbox.get_points()[1]))
        neighborhoods.append((sr.record[3], paths))
    neighborhoods.append(('UNKNOWN', None))

def parseInput():
    # parse data from trip_fare_join data, which excludes head line of the columns
    for line in sys.stdin:
        line = line.strip('\n')
        part1, part2 = line.split('\t')
        values = part1.split(',')
        values.extend(part2.split(','))
        yield values

def mapper():
    index = rtree.Index()
    neighborhoods = []
    readNeighborhood('ZillowNeighborhoods-NY.shp', index, neighborhoods)
    agg = {}
    for values in parseInput():
        if values[10] and values[11] and values[12] and values[13]:
            pickup_location = (float(values[10]), float(values[11]))
            dropoff_location = (float(values[12]), float(values[13]))
            pickup_neighborhood = findNeighborhood(pickup_location, index, neighborhoods)
            dropoff_neighborhood = findNeighborhood(dropoff_location, index, neighborhoods)
            if pickup_neighborhood!=-1 and dropoff_neighborhood!=-1:
                key = neighborhoods[pickup_neighborhood][0] + ',' + neighborhoods[dropoff_neighborhood][0]
                time_of_trips = agg.get(key, [0,0,0])[0] + 1
                total_revenue = agg.get(key, [0,0,0])[1] + float(values[-1])
                tip_amout = agg.get(key, [0,0,0])[2] + float(values[-3])
                agg[key] = [time_of_trips, total_revenue, tip_amout]


    for item in agg.iteritems():
        print '%s\t%d,%.2f,%.2f' % (item[0], item[1][0], item[1][1], item[1][2])


if __name__=='__main__':
    mapper()
