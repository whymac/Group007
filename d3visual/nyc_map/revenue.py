

import matplotlib.pyplot as plt
import numpy as np


li = None
a = []
r1 = []
r2 = []
r3 = []
r4 = []
f = open("data/month.csv")
for line in f:
	li = line
	li = line.split("\r")
for l in li:
	a.append(l.split(","))
for i in a[1:]:
	if i[5] == "1":
			r1.append(float(i[3]))
	elif i[5] == "2":
			r2.append(float(i[3]))
	elif i[5] == "3":
			r3.append(float(i[3]))
	elif i[5] == "4":
			r4.append(float(i[3]))
# print revenue
print [np.percentile(np.array(r1),16),\
	  np.percentile(np.array(r1),32),np.percentile(np.array(r1),48),\
	  np.percentile(np.array(r1),64),np.percentile(np.array(r1),90)],len(r1)

# print [np.percentile(np.array(r2),16),
# 	  np.percentile(np.array(r2),32),np.percentile(np.array(r2),48),\
# 	  np.percentile(np.array(r2),64),np.percentile(np.array(r2),80)]

# print [np.percentile(np.array(r3),16),\
# 	  np.percentile(np.array(r3),32),np.percentile(np.array(r3),48),\
# 	  np.percentile(np.array(r3),64),np.percentile(np.array(r3),80)]

# print [np.percentile(np.array(r4),16),\
# 	  np.percentile(np.array(r4),32),np.percentile(np.array(r4),48),\
# 	  np.percentile(np.array(r4),64),np.percentile(np.array(r4),80)]

# a = np.array([1,1,1,1,1,1000,2000])
# print np.percentile(np.array(a),90)