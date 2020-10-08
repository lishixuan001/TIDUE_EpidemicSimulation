#
# Example program written by Valerie Maxville
#
# SIRmodel.py: Simulate spread of disease through a population 
#              using SIR model 
# 
# Based on SIR model:
#    Shiflet&Shiflet Module 4.3 Modeling the Spread of SARS
#    and https://www.youtube.com/watch?v=k6nLfCbAzgo
#

import matplotlib.pyplot as plt
import numpy as np

Scur = 762   # number of people susceptible
Icur = 1     # number of people infected
Rcur = 0     # number of people recovered

trans_const = 0.00218   # infectiousness of disease r = kb/N
recov_rate = 0.5        # recovery rate a = 1/(# days infected)
simlength = 14          # number of days in simulation

resultarray = np.zeros((simlength+1,3)) # using floats as % of popn
resultarray[0,:] = Scur, Icur, Rcur     # record initial values

for i in range(1, simlength+1):
    new_infected = trans_const * Scur * Icur   # = rSI
    new_recovered = recov_rate * Icur          # = aI

    Scur = Scur - new_infected
    Icur = Icur + new_infected - new_recovered
    Rcur = Rcur + new_recovered

    resultarray[i,:] = Scur, Icur, Rcur

print("\tScur   \t\tIcur    \tRcur")
print(resultarray)

plt.title("SIR Model r = " + str(trans_const) + ", a = " + str(recov_rate))
plt.xlabel("Day")
plt.ylabel("Number of people")
plt.plot(resultarray)
plt.show()   