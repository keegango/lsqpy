"""
Fit a large polynomial to some given data
Play with regularization to understand
Question: Why does increasing regularization not help very much
	near the end of the polynomial (farther from zero)?
"""

# Import lsqpy
from lsqpy import Variable,sum_sq,minimize

# Import the test data
from data import x_data,y_data

# Fit a polynomial of this degree to data
num_powers = 20

# Import matplotlib and create the extra variables we need for plotting
# NumPy imported for matrix manipulation
import numpy as np
import matplotlib.pyplot as plt
plt.plot(x_data,y_data,'bo')
t = np.arange(0,18,0.1).reshape(-1,1)
T = np.hstack([np.power(t,i) for i in range(num_powers)])

# We will regress using different powers of x
X = np.hstack([np.power(x_data,i) for i in range(num_powers)])

# Solve the problem
mu = 0
a = Variable(num_powers)
minimize(sum_sq(X*a - y_data) + mu * sum_sq(a))

# Plot our regressed function
plt.plot(t,T.dot(a.value),'r')
plt.xlabel('x')
plt.ylabel('y')
plt.ylim([-5, 5])
plt.show()
