"""
Do a quadratic fit to the data
"""

# Import lsqpy
from lsqpy import Variable,sum_sq,minimize

# Import the test data
from data import x_data,y_data

# Import matplotlib and create the extra variables we need for plotting
# NumPy imported for matrix manipulation
import matplotlib.pyplot as plt

# Create a variable
a = Variable(3)

# We copy x_data but raise it to different powers
# By treating these new columns as other predictors we can fit a quadratic
# Here we import numpy to help format our data
import numpy as np
X = np.hstack([np.power(x_data,i) for i in range(3)])

# Solve the problem
minimize(sum_sq(X*a - y_data))

# Create some evenly spaced points for plotting, again replicate powers
t = np.arange(0,5,0.1).reshape(-1,1)
T = np.hstack([np.power(t,i) for i in range(3)])

# Plot our regressed function
plt.figure(0,(3,3))
plt.plot(x_data,y_data,'bo')
plt.plot(t,T.dot(a.value),'r')
plt.xlabel('x')
plt.ylabel('y')
plt.show()