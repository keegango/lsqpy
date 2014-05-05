"""
A simple linear regression problem
"""

# Import lsqpy
from lsqpy import Variable,sum_squares,minimize

# Import the test data
from data import x_data,y_data

# Include plotting
import numpy as np
import matplotlib.pyplot as plt

# Solve the problem, and print the result
slope = Variable()
offset = Variable()
minimize(sum_squares(x_data*slope+offset-y_data))
print('slope = '+str(slope.value[0,0])+', offset = '+ str(offset.value[0,0]))

# Print results and plot
t = np.arange(0, 5.0, 0.1)
plt.figure(0,(4,4))
plt.plot(x_data,y_data,'ro')
plt.plot(t,(slope.value[0,0]*t + offset.value[0,0]))
plt.xlabel('x'), plt.ylabel('y')
plt.show()