import sys
import os


def parsefile(filename):
    # parse data
    monthtrip = {}
    trip = {}
    fp = open(filename)
    data = fp.read().strip().split('\n')
    for line in data:
        key, value = line.split('\t')
        pick_up, drop_off= key.split(',')
        time_of_trips, total_revenue, tip_amout = value.split(',')
        try:
            time_of_trips = int(time_of_trips)
            total_revenue = float(total_revenue)
            tip_amout = float(tip_amout)
        except ValueError:
            continue
        trip[key] = [time_of_trips, total_revenue, tip_amout]
    fp.close()
    monthtrip[filename[0:6]] = trip
    return monthtrip

def parsedir(dirname):
    # parse data
    monthtrip = {}
    for files in os.walk('.'+os.sep+dirname):
        for filename in files[2]:
            if filename[:4] == '2013':
                trip = {}
                fp = open('.'+os.sep+dirname+os.sep+filename)
                data = fp.read().strip().split('\n')
                for line in data:
                    key, value = line.split('\t')
                    pick_up, drop_off= key.split(',')
                    time_of_trips, total_revenue, tip_amout = value.split(',')
                    try:
                        time_of_trips = int(time_of_trips)
                        total_revenue = float(total_revenue)
                        tip_amout = float(tip_amout)
                    except ValueError:
                        continue
                    trip[key] = [time_of_trips, total_revenue, tip_amout]
                fp.close()
                monthtrip[filename[0:6]] = trip
    return monthtrip

def sumup(monthtrip):
    pick_agg = {}
    drop_agg = {}
    for t, trip in monthtrip.items():
        for key, value in trip.items():
            pick_up, drop_off = key.split(',')
            time_of_trips = pick_agg.get(pick_up, [0,0,0,0])[0] + value[0]
            total_revenue = pick_agg.get(pick_up, [0,0,0,0])[1] + value[1]
            tip_amout = pick_agg.get(pick_up, [0,0,0,0])[2] + value[2]
            pick_agg[pick_up] = [time_of_trips, float(total_revenue), float(tip_amout), float(round(tip_amout/total_revenue,4))]
            time_of_trips = drop_agg.get(drop_off, [0,0,0,0])[0] + value[0]
            total_revenue = drop_agg.get(drop_off, [0,0,0,0])[1] + value[1]
            tip_amout = drop_agg.get(drop_off, [0,0,0,0])[2] + value[2]
            drop_agg[drop_off] = [time_of_trips, float(total_revenue), float(tip_amout), float(round(tip_amout/total_revenue,4))]
    return([pick_agg,drop_agg])


def writefile(agg):
    if not os.path.exists('.'+os.sep+'pick_drop_summer'):
        os.mkdir('.'+os.sep+'pick_drop_summer')
    f = open('.'+os.sep+'pick_drop_summer'+os.sep+'pickup_'+filename[-10:]+'csv', 'w')
    line = '{},{},{},{},{}\n'.format('pickup neighborhoods','trips number','revenue','tip amount','tip percentage') 
    f.write(line)
    for key, value in agg[0].items():
        line = '{},{},{},{},{}\n'.format(key,value[0],value[1],value[2],value[3]) 
        f.write(line)
    f = open('.'+os.sep+'pick_drop_summer'+os.sep+'dropoff_'+filename[-10:]+'csv', 'w')
    line = '{},{},{},{},{}\n'.format('dropoff neighborhoods','trips number','revenue','tip amount','tip percentage') 
    f.write(line)
    for key, value in agg[1].items():
        line = '{},{},{},{},{}\n'.format(key,value[0],value[1],value[2],value[3]) 
        f.write(line)    
    f.close()

def writefile2(agg):
    if not os.path.exists('.'+os.sep+'pick_drop_summer'):
        os.mkdir('.'+os.sep+'pick_drop_summer')
    f = open('.'+os.sep+'pick_drop_summer'+os.sep+'pickup_summer.csv', 'w')
    line = '{},{},{},{},{}\n'.format('pickup neighborhoods','trips number','revenue','tip amount','tip percentage') 
    f.write(line)
    for key, value in agg[0].items():
        line = '{},{},{},{},{}\n'.format(key,value[0],value[1],value[2],value[3]) 
        f.write(line)
    f = open('.'+os.sep+'pick_drop_summer'+os.sep+'dropoff_summer.csv', 'w')
    line = '{},{},{},{},{}\n'.format('dropoff neighborhoods','trips number','revenue','tip amount','tip percentage') 
    f.write(line)
    for key, value in agg[1].items():
        line = '{},{},{},{},{}\n'.format(key,value[0],value[1],value[2],value[3]) 
        f.write(line)    
    f.close()

def main():
    if len(sys.argv) != 3:
        print 'usage: ./pick_drop_summer.py --file or --directory'
        sys.exit(1)

    option = sys.argv[1]
    global filename

    if option == '--file':  
        filename = sys.argv[2]
        trip = parsefile(filename)
        agg = sumup(trip)
        writefile(agg)

    elif option == '--directory':
        dirname = sys.argv[2]
        trip = parsedir(dirname)
        agg = sumup(trip)
        writefile2(agg)

    else:
        print 'unknown option: ' + option
        sys.exit(1)

if __name__ == '__main__':
    main()
