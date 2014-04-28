import numpy as np

# Set the random seed to get consistent data
np.random.seed(2)

# Number of examples to use
n = 50

# Generate data
x_data = np.random.uniform(size=(n,1))*18
#x_data = np.arange(0,18,0.1).reshape(-1,1)
y_data = (np.sin(x_data*2)
          + np.cos(x_data)
		  - 4*np.cos(x_data)/4
		  + 3*np.sin(x_data/3)
          + 0.2*np.random.standard_normal(size=(x_data.shape[0],1)))

import sys
if(sys.argv[0] == 'data.py'):
	import matplotlib.pyplot as plt
	plt.figure(0)
	plt.plot(x_data,y_data,'bo')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.show()