"""
Loads the data for the tomography example and plots if called directly
"""

from scipy import sparse
import numpy as np

# Load the data with prints to show progress
temps = np.genfromtxt('melbourne_temps.txt')[:,np.newaxis]
n = temps.shape[0]

# Plot data if python was called on this file directly
import sys
if(sys.argv[0] == 'data.py'):
	import matplotlib.pyplot as plt
	plt.figure(0)
	plt.plot(temps,'r')
	plt.show()