import csv

def find_val(col_name, val, target):
    # provide name of the column and a value
    # will search that value in csv file and return the value in the target column
    # if that does not exist, will do interpolation on two adjacent rows to get that value
    with open('sorted.csv', 'r') as file:
        dictreader = csv.DictReader(file, dialect='unix')
        rows = list(dictreader)
    for row in rows:
        if float(row[col_name]) == val:
            return float(row[target])
    # not found, need to interpolate
    for i in range(len(rows)):
        if float(rows[i][col_name]) > val:
            # use this one and previous one
            b1 = float(rows[i][target])
            a1 = float(rows[i-1][target])
            b = float(rows[i][col_name])
            a = float(rows[i-1][col_name])
            result = b1 - (((b1-a1)/(b-a)) * (b-val))
            return result
# print(find_in_csv("Temperature", 294.5, "Enthalpy"))
# print(find_in_csv("Enthalpy", 294.67, "Temperature"))

# Special properties
PA = 101.325 # const
TAI = input("Enter the ambient air temperature: ")
PR = input("Enter the compression ratio: ")
ISENCOM = 0.8
ISENTUR = 0.8
TIT = 1173.15

# State 1
T1 = float(TAI)
P1 = PA
Pr1 = find_val("Temperature", T1, "Reduced Pressure")
h1 = find_val("Temperature", T1, "Enthalpy")

# State 2
#P2 = float(PR) * P1
Pr2 = float(PR) * Pr1
T2s = find_val("Reduced Pressure", Pr2, "Temperature")
h2s = find_val("Reduced Pressure", Pr2, "Enthalpy")
h2a = ((h2s-h1)/ISENCOM) + h1

# State 3
T3 = TIT
h3 = find_val("Temperature", T3, "Enthalpy")
Pr3 = find_val("Temperature", T3, "Reduced Pressure")

# Heat injection between State 2 and State 3
QIN = h3 - h2a

# State 4
Pr4 = Pr3/float(PR)
h4s = find_val("Reduced Pressure", Pr4, "Enthalpy")
T4s = find_val("Reduced Pressure", Pr4, "Temperature")
h4a = h3 - (ISENTUR * (h3 - h4s))
T4a = find_val("Enthalpy", h4a, "Temperature")

# Actual work done of compressor
WC = h2a -h1
print("Work done of compressor: ", WC)

# Actual work done of turbine
WT = h3 - h4a
print("Work done of turbine: ", WT)

# Thermal efficiency of the turbine
Eff = (WT - WC) * 100/QIN
print("Thermal Efficiency", Eff)

#Sample
print(h1, h2a, h3, h4a)