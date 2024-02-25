import csv

col_name = input("Enter the name of property: ")
value = input("Enter the value: ")
val = float(value)
target = input("Enter the target name: ")
    # provide name of the column and a value
    # will search that value in csv file and return the value in the target column
    # if that does not exist, will do interpolation on two adjacent rows to get that value
with open('sorted.csv', 'r') as file:
    dictreader = csv.DictReader(file, dialect='unix')
    rows = list(dictreader)
    for row in rows:
        if float(row[col_name]) == val:
            print(float(row[target]))
    # not found, need to interpolate
    for i in range(len(rows)):
        if float(rows[i][col_name]) > val:
            # use this one and previous one
            b1 = float(rows[i][target])
            a1 = float(rows[i-1][target])
            b = float(rows[i][col_name])
            a = float(rows[i-1][col_name])
            result = b1 - (((b1-a1)/(b-a)) * (b-val))
            break
    print(result)