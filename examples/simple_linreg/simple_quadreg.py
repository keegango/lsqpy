"""
Do a quadratic fit to the data
"""

# Import lsqpy
from lsqpy import Variable,sum_squares,minimize

# Import the test data
from data import x_data,y_data

# Create variables that holds the coefficients
quadratic = Variable()
slope = Variable()
offset = Variable()

# We copy x_data but square the entries
import numpy as np
x_squared = np.power(x_data,2)

# Solve the problem
minimize(sum_squares(offset + x_data*slope + x_squared*quadratic - y_data))

# Create some evenly spaced points for plotting, again replicate powers
t = np.arange(0,5,0.1).reshape(-1,1)
t_squared = np.power(t,2)

# Plot our regressed function
import matplotlib.pyplot as plt
plt.figure(0,(4,4))
plt.plot(x_data,y_data,'ro')
plt.plot(t,offset.value[0,0] + t*slope.value[0,0] + t_squared*quadratic.value[0,0],'b')
plt.xlabel('x')
plt.ylabel('y')
plt.show()