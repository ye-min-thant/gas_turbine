import csv
import operator
with open('data_parse.csv',newline='') as csvfile:
    spamreader = csv.DictReader(csvfile, delimiter=",")
    sortedlist = sorted(spamreader, key=lambda row:int(row['Temperature']), reverse=False)

with open('sorted.csv', 'w') as f:
    fieldnames = ["Temperature","Enthalpy","Reduced Pressure","Internal Energy","Specific Volume","Entropy"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in sortedlist:
        print(row)
        writer.writerow(row)
