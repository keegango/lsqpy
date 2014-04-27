"""
A simple regression problem
"""

# Import lsqpy
from lsqpy import Variable,sum_sq,minimize

# Import the test data
from data import x_data,y_data

# Solve the problem, and print the result
slope = Variable()
offset = Variable()
minimize(sum_sq(x_data*slope+offset-y_data))
print('slope = '+str(slope.value[0,0])+', offset = '+ str(offset.value[0,0]))

# Include plotting
import numpy as np
import matplotlib.pyplot as plt

# Print results and plot
t = np.arange(0, 5.0, 0.1)
plt.figure(0,(3,3))
plt.plot(x_data,y_data,'ro')
plt.plot(t,(slope.value[0,0]*t + offset.value[0,0]))
plt.xlabel('x'), plt.ylabel('y')
plt.show()