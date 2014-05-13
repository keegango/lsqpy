import numpy as np
from lsqpy import Variable,solve

A = np.zeros((3,3))
print(A)

b = np.array([[1,0,3]]).T
print(b)

x = Variable(3)
solve([A*x == b])
print(x.value)