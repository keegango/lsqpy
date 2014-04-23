import numpy as np

# Set the random seed to get consistent data
np.random.seed(0)

# Number of examples to use
n = 100

# Specify the true value of the variable
true_slope = 2
true_offset = -10

# Generate data
x_data = np.random.uniform(size=(n,1))*5
y_data = true_slope*x_data+true_offset + np.random.standard_normal(size=(n,1))


# Plot data if python was called on this file directly
import sys
if(sys.argv[0] == 'data.py'):
	import matplotlib.pyplot as plt
	plt.figure(0,(3,3))
	plt.plot(x_data,y_data,'ro')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.show()