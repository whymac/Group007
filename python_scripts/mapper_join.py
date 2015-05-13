#!/usr/bin/python

import sys
import string
import os


# input comes from STDIN (stream data that goes to the program)
for line in sys.stdin:
    
    # remove numbers and punctuation
    l = line.strip()
    w = l.split(',' , )

    if (len(w) == 11):
        if w[0] != 'medallion':
            key = ','.join(w[0:4])
            value = ','.join(w[4:len(w)])
            print "%s\t%s" % (key,value)

    if (len(w) == 14):
        if w[0] != 'medallion':
            key = ','.join((w[0],w[1],w[2],w[5]))
            value = ','.join((w[3],w[4],','.join(w[6:len(w)])))
            print "%s\t%s" % (key,value)
 


 

 

        
        # output goes to STDOUT (stream data that the program writes)