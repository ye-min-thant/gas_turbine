import csv
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('_mpl-gallery')


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
TAI = input("Enter the ambient air temperature: ")
PR = input("""Enter the compression ratio (Enter a range in this form "start,stop" with no space in between): """)
PA = 101.325  # const
ISENCOM = float(input("Enter the compressor effiency: "))
ISENTUR = float(input("Enter the turbine effiency: "))
TIT = float(input("Enter turbine inlet temperature: "))
PR = np.arange(float(PR.split(',')[0]), float(PR.split(',')[1]), 0.1).tolist()


# State 1
def calculate_efficiency(TAI, PR, ISENCOM, ISENTUR, TIT,):
    T1 = float(TAI)
    # P1 = PA
    Pr1 = find_val("Temperature", T1, "Reduced Pressure")
    h1 = find_val("Temperature", T1, "Enthalpy")

# State 2
    Pr2 = float(PR) * Pr1
    # T2s = find_val("Reduced Pressure", Pr2, "Temperature")
    h2s = find_val("Reduced Pressure", Pr2, "Enthalpy")
    h2a = ((h2s-h1)/ISENCOM) + h1

# State 3
    T3 = TIT
    h3 = find_val("Temperature", T3, "Enthalpy")
    Pr3 = find_val("Temperature", T3, "Reduced Pressure")

# Heat injection between State 2 and State 3
    QIN = h3 - h2a

# State 4
    Pr4 = Pr3/PR
    h4s = find_val("Reduced Pressure", Pr4, "Enthalpy")
    # T4s = find_val("Reduced Pressure", Pr4, "Temperature")
    h4a = h3 - (ISENTUR * (h3 - h4s))
    # T4a = find_val("Enthalpy", h4a, "Temperature")

# Actual work done of compressor
    WC = h2a - h1

# Actual work done of turbine
    WT = h3 - h4a

# Thermal efficiency of the turbine
    Eff = (WT - WC) * 100/QIN
    return Eff

thermal_efficiencies = []
for pressure in PR:
    thermal_efficiencies.append(
            calculate_efficiency(TAI, pressure, ISENCOM, ISENTUR, TIT)
            )
MAX = max(thermal_efficiencies)
for i in range(len(thermal_efficiencies)):
    if MAX == thermal_efficiencies[i]:
        pr_max_eff = PR[i]
print("Pressure ratio at maximum efficiency: ", pr_max_eff)
print("Maximum thermal efficiency: ", MAX)

#fig, ax = plt.subplots()
#ax.plot(PR, thermal_efficiencies, linewidth=2.0)
plt.plot(PR, thermal_efficiencies, '-')
plt.plot(pr_max_eff, MAX, 'x', ms = 20, mec = 'r')

plt.title("Pressure Ratio Vs Thermal Efficiencies")
plt.xlabel("Pressure Ratio")
plt.ylabel("Thermal Efficiency")
plt.show()
#plt.plot(x[:i-1], y[:i-1], "something")
#plt.plot(x[i], y[i], "another thing")
#plt.plot(x[i+1:], y[i+1:], "soomething" )`