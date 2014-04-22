"""
A simple classifier
"""

from lsqpy.exprs.variable import Variable
from lsqpy.exprs.sum_sq import sum_sq
from lsqpy.minimize import minimize

# For plotting
import numpy as np
import matplotlib.pyplot as plt

# Import the test data
# n is the number of data points
# x_data is n x 1, as is y_data
from data import n,x_data,y_data

# Solve the problem, and print the result
slope = Variable()
offset = Variable()
minimize(sum_sq(x_data*slope+offset.broadcast(n,1)-y_data))
slope.value
offset.value

t = np.arange(0, 5.0, 0.1)

plt.plot(x_data,y_data,'ro')
plt.plot(t,(slope.value[0,0]*t + offset.value[0,0]))
plt.xlabel('x')
plt.ylabel('y')
plt.show()