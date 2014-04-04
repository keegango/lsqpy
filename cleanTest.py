"""
Do some full tests of the system
"""

# Collect these so that there are fewer imports?
from lsqpy.exprs.variable import Variable
from lsqpy.exprs.normsq import normsq
from lsqpy.minimize import minimize
import numpy as np

# Examples of combining
z = Variable(2)
z + 2
z + np.array([[1],[2]])
z + np.array([[1,2],[3,4]]) # Basic size checking
2 + z # Both directions
2*z - np.array([[1],[2]]) # Scaling and subtraction

# Multiplication
A = np.array([[1,2],[3,4]])
A*z
z*A # Checks on size

# Multiple variables
x = Variable(3)
y = Variable(2)
x + y # Fails
z + y
A*z+A*y
A*(z+y)

# Slicing
A*x # Fails
A*x.slice([1,2])

# Equality constraints
A*z == 2
A*z == y
(z+0) == y # Need a hack here because override variable '==' so we can hash

# Create a small test problem
x = Variable(4)
A = np.array([[1,2,3,10],[5,4,6,11],[9,7,8,12]]);
b = np.array([[16],[26],[36]])
minimize(normsq(x),[A*x == b])
print(x.value())

# Create a small test problem
x = Variable(4)
minimize(normsq(A*x+b),[x.slice([2,3]) == 100])
print(x.value())

# A regularization problem
x = Variable(4)
minimize(normsq(A*x+b)+100*normsq(x),[x.slice([2,3]) == 100])
print(x.value())