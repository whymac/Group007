import csv

num = [["dim1","dim2"]]
for i in range(1,11):
	for j in range(1,11):
		num.append([i,j])

with open('heat.tsv', 'w') as fp:
    a = csv.writer(fp, delimiter='\t')
    a.writerows(num)