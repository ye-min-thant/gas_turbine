import csv

with open('data.txt', 'r+') as file:
    csv_rows = []
    lines = file.readlines()
    for line in lines:
        first_part = line.split()[:6]
        second_part = line.split()[6:]
        csv_rows.append(first_part)
        if second_part:
            csv_rows.append(second_part)

with open('data_parse.csv', 'w+') as file_handle:
    writer = csv.writer(file_handle, dialect='unix')
    for row in csv_rows:
        writer.writerow(row)