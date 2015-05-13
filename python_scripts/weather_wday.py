#!/usr/bin/env python
import sys
import numpy, time
import os


def parseWeather(dirname):
    # parse data
    global weather
    weather = {}
    for files in os.walk('.'+os.sep+dirname):
        for filename in files[2]:
            if filename[-11:] == 'weather.csv':
                fp = open('.'+os.sep+dirname+os.sep+filename)
                data = fp.read().strip().split('\n')
                for line in data:
                    l = line.split(',')

                    if l[21] != ' Events':
                        if l[21] in ('Rain','Snow','Rain-Snow','Fog-Rain','Fog-Snow','Fog-Rain-Snow'):
                            weather[time.strptime(l[0], '%Y-%m-%d')] = 'rain'
                        else:
                            weather[time.strptime(l[0], '%Y-%m-%d')] = 'no_rain'

    return weather

def parseDay(dirname):
    pair = {}
    for files in os.walk('.'+os.sep+dirname):
        for filename in files[2]:
            if filename[-4:] == 'year':
                fp = open('.'+os.sep+dirname+os.sep+filename)
                data = fp.read().strip().split('\n')
                for line in data:
                    key, value = line.split('\t')
                    date = time.strptime(key, '%Y-%m-%d')
                    time_of_trips, total_revenue, tip_amout, tip_percentage = value.split(',')
                    try:
                        time_of_trips = int(time_of_trips)
                        total_revenue = float(total_revenue)
                        tip_amout = float(tip_amout)
                    except ValueError:
                        continue
                    if wday(key) == 'weekdays' and weather[date] == 'rain':
                        time_of_trips = pair.get('weekdays_rain', [0,0,0,0,0,0])[0] + time_of_trips
                        total_revenue = pair.get('weekdays_rain', [0,0,0,0,0])[1] + total_revenue
                        tip_amout = pair.get('weekdays_rain', [0,0,0,0,0])[2] + tip_amout
                        index = pair.get('weekdays_rain', [0,0,0,0,0])[4] + 1
                        pair['weekdays_rain'] = [time_of_trips, float(total_revenue), float(tip_amout), float(round(tip_amout/total_revenue,4)),index]
                    elif wday(key) == 'weekdays' and weather[date] == 'no_rain':
                        time_of_trips = pair.get('weekdays_no_rain', [0,0,0,0,0])[0] + time_of_trips
                        total_revenue = pair.get('weekdays_no_rain', [0,0,0,0,0])[1] + total_revenue
                        tip_amout = pair.get('weekdays_no_rain', [0,0,0,0,0])[2] + tip_amout       
                        index = pair.get('weekdays_no_rain', [0,0,0,0,0])[4] + 1                
                        pair['weekdays_no_rain'] = [time_of_trips, float(total_revenue), float(tip_amout), float(round(tip_amout/total_revenue,4)),index]
                    elif wday(key) == 'weekends&holidays' and weather[date] == 'rain':
                        time_of_trips = pair.get('weekends&holidays_rain', [0,0,0,0,0])[0] + time_of_trips
                        total_revenue = pair.get('weekends&holidays_rain', [0,0,0,0,0])[1] + total_revenue
                        tip_amout = pair.get('weekends&holidays_rain', [0,0,0,0,0])[2] + tip_amout
                        index = pair.get('weekends&holidays_rain', [0,0,0,0,0])[4] + 1                       
                        pair['weekends&holidays_rain'] = [time_of_trips, float(total_revenue), float(tip_amout), float(round(tip_amout/total_revenue,4)),index]
                    elif wday(key) == 'weekends&holidays' and weather[date] == 'no_rain':
                        time_of_trips = pair.get('weekends&holidays_no_rain', [0,0,0,0,0])[0] + time_of_trips
                        total_revenue = pair.get('weekends&holidays_no_rain', [0,0,0,0,0])[1] + total_revenue
                        tip_amout = pair.get('weekends&holidays_no_rain', [0,0,0,0,0])[2] + tip_amout
                        index = pair.get('weekends&holidays_no_rain', [0,0,0,0,0])[4] + 1                       
                        pair['weekends&holidays_no_rain'] = [time_of_trips, float(total_revenue), float(tip_amout), float(round(tip_amout/total_revenue,4)),index]
    return pair

def writefile(pair):
    if not os.path.exists('.'+os.sep+'weather&weekday'):
        os.mkdir('.'+os.sep+'weather&weekday')
    f = open('.'+os.sep+'weather&weekday'+os.sep+'weather&weekday.csv' , 'w')
    line = '{},{},{},{},{}\n'.format('','time of trips','revenue','tip amount','tip percentage')
    f.write(line)
    for key, value in pair.items():
        line = '{},{},{},{},{}\n'.format(key,value[0]/value[4],value[1]/value[4],value[2]/value[4],float(round(value[2]/(value[1]-value[2]),4)))
        f.write(line)
    f.close()


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
    holiday_list = ['01-01','01-21','02-12','02-18','05-27','07-04','09-02','10-14','11-05','11-11','11-28','11-29','12-24','12-25']
    dirname = sys.argv[1]
    parseWeather(dirname)
    writefile(parseDay(dirname))
                
if __name__=='__main__':
    main()
