from lsqpy.exprs.variable import Variable
from lsqpy.exprs.normsq import normsq
from lsqpy.minimize import minimize

import numpy as np

import sys

test_num = int(sys.argv[1])

if test_num == 1:
	print('basic problem')
	x = Variable(4)
	A = np.array([[1,2,3,10],[5,4,6,11],[9,7,8,12]]);
	b = np.array([[16,26,36]]).T
	minimize(normsq(x),[A*x == b])
	print(x.getValue())

elif test_num == 2:
	print('another basic problem')
	x = Variable(4)
	A = np.array([[1,2,3,10],[5,4,6,11],[9,7,8,12]]);
	b = np.array([[16,26,36]]).T
	objective = normsq(A*x+b)+100*normsq(x)
	constraint = x[2:4] == 100
	minimize(objective,[constraint])
	print(x.getValue())