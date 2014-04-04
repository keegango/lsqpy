"""
Try some problems of various size
"""

from lsqpy.affine import Affine
from lsqpy.variable import Variable
from lsqpy.problem import Problem
import numpy as np
from numpy.random import rand

# Set the size of the problem
scale = 1
m = 100
n = 5000

# Generate an equality constraint A*x = b
print('generating data')
A = 10*rand(m,n)
x_val = rand(n,1)
b = A.dot(x_val)

# Solve a problem
print('begin solving of data')
x = Variable(n)
p = Problem(x)
eq_const = (b == A*x)
p.addEqConst(eq_const)
p.solve()