"""
Reads a temperature data file as taken from
http://www.cru.uea.ac.uk/cru/data/temperature/
"""

import numpy as np
import matplotlib.pyplot as plt
import sys

data_file = open('CRUTEM4v-gl.dat')

# We want to only extract the even lines (0 indexed)
parity = 0
years = []
temperatures = []
for line in data_file:
	if(parity % 2 == 0):
		line_split = line.split()
		years.append(int(line_split[0]))
		temperatures += [float(t) for t in line_split[1:-1]]
	parity += 1

# Done reading file
data_file.close()

# Quantities to be imported
begin_year = years[0]
temperatures = np.array([temperatures]).T
num_samples = temperatures.shape[0]

# Plot data if python was called on this file directly
if(sys.argv[0] == 'data.py'):
	plt.figure(0)
	plt.plot(temperatures)
	plt.ylabel('temperatures')
	plt.show()