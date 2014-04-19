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
from data import X,y,n

# Solve the problem, and print the result
a = Variable(2)
minimize(sum_sq(X*a-y),[])
print(a.getValue())

# Plot the line we found
plt.plot(X[y[:,0]>=0,0],X[y[:,0]>=0,1],'ro')
plt.plot(X[y[:,0]<0,0],X[y[:,0]<0,1],'bo')

t = np.arange(-5.0, 5.0, 0.1)

plt.plot(t,(-a.getValue()[0,0]*t)/a.getValue()[1,0])
plt.xlabel('x')
plt.ylabel('y')
plt.show()