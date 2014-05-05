"""
A simple classifier
"""

# Import lsqpy
from lsqpy import Variable, sum_squares, minimize

# For plotting
import numpy as np
import matplotlib.pyplot as plt

# Import the test data
from data import X,y,n

# Solve the problem, and print the result
a = Variable(2)
minimize(sum_squares(X*a-y),[])
print(a.value)

# Plot the line we found
plt.plot(X[y[:,0]>=0,0],X[y[:,0]>=0,1],'ro')
plt.plot(X[y[:,0]<0,0],X[y[:,0]<0,1],'bo')

t = np.arange(-5.0, 5.0, 0.1)

plt.plot(t,(-a.value[0,0]*t)/a.value[1,0])
plt.xlabel('x')
plt.ylabel('y')
plt.show()