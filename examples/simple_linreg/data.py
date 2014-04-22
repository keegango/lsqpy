import numpy as np

# Set the random seed to get consistent data
np.random.seed(0)

# Number of examples to use
n = 100

# Specify the true value of the variable
true_square = 2
true_slope = 2
true_offset = -10

# Scaling
noise_scale = 1
x_scale = 5

# Create data and labels
x_data = np.random.uniform(size=(n,1))*x_scale
y_data = true_slope*x_data+true_offset + np.random.standard_normal(size=(n,1))*noise_scale

# Create some quadratic data
x_sq_data = np.random.uniform(size=(n,1))*x_scale
y_sq_data = (true_square*x_sq_data*x_sq_data+ true_offset*x_sq_data
            + np.random.standard_normal(size=(n,1))*noise_scale)

# Plot data if python was called on this file directly
import sys
if(sys.argv[0] == 'data.py'):
	import matplotlib.pyplot as plt
	plt.plot(x_data,y_data,'ro')
	if len(sys.argv) >= 2 and sys.argv[1] == 'square':
		plt.plot(x_sq_data,y_sq_data,'bo')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.show()