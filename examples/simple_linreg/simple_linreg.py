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
from data import x_data,y_data,n

# Solve the problem, and print the result
slope = Variable()
offset = Variable()
minimize(sum_sq(x*slope-y),[])
print(a.value)

t = np.arange(0, 10.0, 0.2)

plt.plot(x_data,y_data,'ro')
plt.plot(t,(-a.value[0,0]*t)/a.value[1,0])
plt.xlabel('x')
plt.ylabel('y')
plt.show()