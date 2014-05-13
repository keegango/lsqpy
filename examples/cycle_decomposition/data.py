"""
Load the black forest temperature data set
from data import times,temps,n,days
"""

import numpy as np

# Useful command to read a (space)delimited file
# Check out the documentation
temps = np.genfromtxt('bf_data.txt')
times = temps[:,0:1].astype(int)
temps = temps[:,1:2]

n = temps.shape[0] # The number of datapoints
days = int(np.max(times))+1 # Number of days to represent