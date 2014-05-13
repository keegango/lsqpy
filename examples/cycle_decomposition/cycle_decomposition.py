"""
Example of fitting a general cyclic function to some data
and handling the residuals with a auto-regressive model.
"""
# Import lsqpy
from lsqpy import Variable,sum_squares,minimize

# Import our data
from data import times, temps, n, days

# Import other libraries for plotting
import numpy as np
import matplotlib.pyplot as plt

import cProfile, pstats, io
pr = cProfile.Profile()
pr.enable()	

# Create our variables
season_cycle = Variable(days)

constraints = []
# Create constraints to model yearly temperature cycle
print('begin creating constraints')
for i in range(365,days): constraints.append(season_cycle[i] == season_cycle[i-365])
print('done creating constraints')

# Create an objective, requires indexing since temps has missing time points
print('begin creating objective')
objective = sum_squares([season_cycle[int(times[i,0])] - temps[i,0] for i in range(n)])
objective += 50*sum_squares(season_cycle[0:days-1]-season_cycle[1:days])
print('done creating objective')

# Solve
minimize(objective,constraints)

pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())

# Plot
print('begin plot')
plt.figure(0,(20,4))
plt.plot(times,temps,'bo')
t = np.arange(0,days,1).reshape(-1,1)
plt.plot(t,season_cycle.value,'r-')
plt.xlim(1000,3000)
plt.show()
print('done plot')