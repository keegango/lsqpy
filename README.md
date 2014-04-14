#lsqpy

lsqpy is a library that makes it easy to formulate and solve least-squares optimization problems with linear constraints. With lsqpy, these types of problems can be created using a natural syntax for variables, constraints, and objectives that mirror standard mathematical notation.

##There is more!
lsqpy's syntax and format are modelled on those of cvxpy, another python library that handles the larger class of convex optimization problem.

See cvxpy here: https://github.com/cvxgrp/cvxpy

##Getting Started
lsqpy only has a few types of objects that you need to work with. Here is an example of a small program.

    # Generate some data for a small example
	A = numpy.array(range(12)).reshape(4,3)
	b = numpy.array([[8,15,4,3]]).T
	
	x = Variable(3)                             # Create a variable
	expression = A*x + b                        # Create an affine
	objective = sumsq(expression) + 10*sumsq(x) # Create an objective
	constraint = x[2] == 20                     # Create an equality constraint
	minimize(objective,[constraint])            # Solve the problem
	print(x.getValue())                         # Display the results

### Variables

	x = Variable(3)                             # Create a variable (3x1)
	y = Variable()                              # A scalar variable (1x1)
	z = Variable(10,4)                          # A matrix variable (10x4)

Variables are the start of all lsqpy expressions. They can be a scalar, a vector, or a matrix.

### Affine Expressions

	expression = A*x + b                        # Create an affine

Affine expressions are built from variables and constants. In particular an affine expression can be created in any of the following ways:
* Two variables are added or subtracted
* A variable is added, subtracted, or multiplied by a constant (scalar or matrix)
* Two affine expressions are added or subracted
* An affine expression is added, subtracted, or multiplied by a constant (scalar or matrix)

For example, in the above code the variable x is first multiplied by the matrix A (a constant) producing an affine expression. That expression is then added to b to produce the final affine expression which is stored as the 'expression' for later use.

Remember that all affine expressions, and variables as well, have dimensions and can only be combined with appropriately sized expressions.

### Sum of Sqaures (sumsq) Expressions

	objective = sumsq(expression) + 10*sumsq(x) # Create an objective

lsqpy handles objectives that are formed by summing the squares of the entries of an affine expression. As in the example above, a sumsq expression is formed by first creating a variable or affine expression then calling the function sumsq() on it. sumsq expressions can also be combined in two ways:
* The sum of two sumsq expressions is also a sumsq expression
* A sumsq expression can be multiplied by a positive scalar to produce a new sumsq expression

### Equality Constraints

	constraint = x[2] == 20                     # Create an equality constraint

Constraints are created with the '==' operation. These constraints can be formed in the following situations:
* variable == constant : A variable may be set equal to a constant (scalar or matrix, see note)
* variable == affine : A variable may be set equal to an affine expression
* affine == constant : Again, the constant maybe a scalar or a matrix (see note)
* affine == affine : Affine expressions may be set equal to each other

Note: the left hand side of the equality is expected to have the same dimensions as the right hand side. For instance, a 4x3 affine expression can only be set equal to a constant, variable, or affine that is also 4x3. There is one exception that setting a variable or affine equal to a scalar creates an equality constraint that enforces all entries are equal to that scalar - this is known as broadcasting and is simply for convenience.

### Solving the problem

	minimize(objective,[constraint])            # Solve the problem
	print(x.getValue())                         # Display the results

The 'minimize' function is called when it is time to solve the least-squares problem you have created. It takes as arguments an objective that is a sumsq expression, and a list of equality constraints to apply. The function will then attempt to solve. If a solution is found, the value of a variable can be obtained by calling the method getValue() on the variable.

There are two cases where 'minimize' will be unable to solve the problem. The first is when the system is over-determined ... The system may also be under-determined in which case ...

## Another Example

The following block of code solves a basic control problem in which we wish to find a series of inputs that allow us to reach waypoints along a path at certain times while minimize fuel use. The position at time i can be described as

TODO: inset math properly

x(i+1) = A*x(i) + b*u(i) and the fuel use is sum(u(i)^2).

The problem can be solved with the following code

    # Define the state and input matrices
	A = np.array([[1, 0.5],[0, 2]])
	b = np.array([[0.4, 0.5]]).T
	
	# Set level of discretization
	T = 100
	
	# Set some way points at T/4 intervals
	x0 = np.array([[0, 0]]).T
	xq1 = np.array([[10, 6]]).T
	xh1 = np.array([[-14,-3]]).T
	xq3 = np.array([[5,10]]).T
	xf = x0
	
	# Create variables
	x = Variable(2,T+1)
	u = Variable(T)
	
	# Create equality constraints
	eq_constraints = []
	# Add time update constraints
	for i in range(T): eq_constraints.append(x[:,i+1] == A*x[:,i] + b*u[i])
	# Add waypoint constraints
	eq_constraints.append(x[:,0] == x0)
	eq_constraints.append(x[:,T//4] == xq1)
	eq_constraints.append(x[:,T//2] == xh1)
	eq_constraints.append(x[:,3*T//4] == xq3)
	eq_constraints.append(x[:,T] == xf)
	
	# Create objective, we also minimize x to ensure our path
	# doesn't take us too far from the origin
	objective = sumsq(x)+100*sumsq(u)
	
	# Solve the problem and print our control vector
	minimize(objective,eq_constraints)
	print(u.getValue())

## Installing lsqpy

Tested on python 3.(3,4) and using the newest versions of numpy and scipy for these python versions.

TODO
