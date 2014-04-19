import numpy as np

# Set the random seed to get consistent data
np.random.seed(0)

# Number of examples to use
n = 200

# Specify the true value of the variable
true_vect = np.array([[-1,1]]).T

# Create data and labels
X = np.random.standard_normal(size=(n,2))*2
y = np.sign(X.dot(true_vect)+np.random.standard_normal(size=(n,1)))

# Plot data if python was called on this file directly
import sys
if(sys.argv[0] == 'data.py'):
	import matplotlib.pyplot as plt
	plt.plot(X[y[:,0]>=0,0],X[y[:,0]>=0,1],'ro')
	plt.plot(X[y[:,0]<0,0],X[y[:,0]<0,1],'bo')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.show()