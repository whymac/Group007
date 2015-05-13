#!/usr/bin/env python
import sys
import numpy, time
import os


def parsedir(dirname):
    # parse data
    if not os.path.exists('.'+os.sep+'avg trips per day'):
        os.mkdir('.'+os.sep+'avg trips per day')
    f = open('.'+os.sep+'avg trips per day'+os.sep+'avg trips per day.csv' , 'w')
    line = '{},{},{}\n'.format('month','weekdays','weekends&holidays') 
    f.write(line)
    for files in os.walk('.'+os.sep+dirname):
        for filename in files[2]:
            if filename[-3:] == 'day':
                trip = {}
                fp = open('.'+os.sep+dirname+os.sep+filename)
                data = fp.read().strip().split('\n')
                dates = []
                stat = {'weekdays':0,'weekends&holidays':0}
                pair = {}
                sumup = {'weekdays':0,'weekends&holidays':0}
                for line in data:
                    key, value = line.split('\t')
                    num = value.split(',')[0]
                    try:
                        num = int(num)
                    except ValueError:
                        continue
                    dates.append(key)
                    pair[key] = num
                for date in dates:
                    if wday(date) == 'weekdays':
                        stat['weekdays'] = stat.get('weekdays') + 1
                        sumup['weekdays'] = sumup.get('weekdays') + pair[date]
                    else:
                        stat['weekends&holidays'] = stat.get('weekends&holidays') + 1
                        sumup['weekends&holidays'] = sumup.get('weekends&holidays') + pair[date]
                line = '{},{},{}\n'.format(filename[:6],float(sumup['weekdays']/stat['weekdays']),float(sumup['weekends&holidays']/stat['weekends&holidays']))
                f.write(line)
                fp.close()
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
    parsedir(dirname)
                
if __name__=='__main__':
    main()
