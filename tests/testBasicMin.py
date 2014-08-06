from lsqpy import Variable,sum_squares,minimize

import numpy as np

import sys

test_num = int(sys.argv[1])

if test_num == 1:
	print('basic problem')
	x = Variable(4)
	A = np.array([[1,2,3,10],[5,4,6,11],[9,7,8,12]]);
	b = np.array([[16,26,36]]).T
	minimize(sum_squares(x),[A*x == b])
	print(x.value)

elif test_num == 2:
	print('another basic problem')
	x = Variable(4)
	A = np.array([[1,2,3,10],[5,4,6,11],[9,7,8,12]]);
	b = np.array([[16,26,36]]).T
	objective = sum_squares(A*x+b)+100*sum_squares(x)
	const_val = np.array([[100,100]]).T
	constraint = const_val == x[2:4]
	minimize(objective,[constraint])
	print(x.value)

elif test_num == 3:
	print('really concise test')
	# Generate some data for a small example
	A = np.array(range(12)).reshape(4,3)
	b = np.array([[8,15,4,3]]).T
	# Create a variable
	x = Variable(3)
	# Create an affine
	affine_expression = A*x + b
	# Create a sum_squares to use for the objective
	objective = sum_squares(affine_expression) + 10*sum_squares(x) 
	# Create an equality constraint
	constraint = x[2] == 20
	# Solve the problem
	minimize(objective,[constraint]) 
	print(x.value)

elif test_num == 4:
	# Define the state and input matrices
	A = np.array([[1, 0.5],[0, 2]])
	b = np.array([[0.4, 0.5]]).T
	
	# Set some way points
	x0 = np.array([[0, 0]]).T
	xq1 = np.array([[10, 6]]).T
	xh1 = np.array([[-14,-3]]).T
	xq3 = np.array([[5,10]]).T
	xf = x0
	
	# Set level of discretization
	T = 100
	
	# Create variables
	x = Variable(2,T+1)
	u = Variable(T)
	
	# Create equality constraints
	eq_constraints = []
	for i in range(T): eq_constraints.append(x[:,i+1] == A*x[:,i] + b*u[i])
	eq_constraints.append(x[:,0] == x0)
	eq_constraints.append(x[:,T//4] == xq1)
	eq_constraints.append(x[:,T//2] == xh1)
	eq_constraints.append(x[:,3*T//4] == xq3)
	eq_constraints.append(x[:,T] == xf)
	
	# Create objective
	objective = sum_squares(x)+100*sum_squares(u)
	
	# Solve the problem and print our control vector
	minimize(objective,eq_constraints)
	print(u.value)
	
elif test_num == 5:
	A = np.array(range(12)).reshape(4,3)
	b = np.array([[8,15,4,3]]).T
	x = Variable(3)
	minimize(sum_squares(A*x + b) + 10*sum_squares(x) ,[x[2] == 20])
	print(x.value)

elif test_num == 6:
	A = np.array(range(12)).reshape(4,3)
	b = np.array([[8,15,4,3]]).T
	x = Variable(3)
	minimize(sum_squares(A*x + b) + 10*sum_squares(x) ,[sum(x) == 10])
	print(x.value)

elif test_num == 7:
	A = np.array(range(12)).reshape(4,3)
	b = np.array([[8,15,4,3]]).T
	x = Variable(3)
	minimize(sum_squares(A*x + b) + 10*sum_squares(x) ,[sum(x) == 10])
	print(x.value)
	
	y = Variable(3)
	minimize(sum_squares(A*y + b) + 10*sum_squares(y) ,[sum(y) == 10])
	print(y.value)
	
	minimize(sum_squares(A*y + b) + 15*sum_squares(y) + 1*sum_squares(x), [sum(y) == 10])
	print(x.value)
	print(y.value)
	