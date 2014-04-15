#lsqpy

lsqpy is a library that makes it easy to formulate and solve least-squares optimization problems with linear equality constraints. With lsqpy, these types of problems can be created using a natural syntax for variables, constraints, and objectives that mirror standard mathematical notation.

lsqpy's syntax and format are modelled on those of [cvxpy](https://github.com/cvxgrp/cvxpy "cvxpy"), a python library that handles the larger class of convex optimization problems.

##Getting Started

Here is an introductory example to lsqpy.

  	A = np.array(range(12)).reshape(4,3)
	b = np.array([[8,15,4,3]]).T
    
	x = Variable(3) # a variable vector of length 3
	minimize(sumsq(A*x + b) + 10*sumsq(x) ,[x[2] == 20])
	print(x.getValue())

In this example, x is our unknown variable that we wish to solve for. The function 'minimize' takes two arguments: an objective to minimize, and a list of linear equality constraints that must be satisfied. Our goal is to find which x makes the objective as small as possible, while still obeying the constraints. Running the above code prints:

	Begin minimization
	Solved, value = 9005.03
	[[ -8.61 ]
	 [-15.035]
	 [ 20.   ]]

As we expected we found a value for x which clearly satisfies our constraint. Less obviously, this is the x which minimizes our objective as well.

## Installing lsqpy

TODO

## Full Specification
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

### Equality Constraints

	constraint = x[2] == 20                     # Create an equality constraint

Constraints are created with the '==' operation. These constraints can be formed in the following situations:
* variable == constant : A variable may be set equal to a constant (scalar or matrix, see note)
* variable == affine : A variable may be set equal to an affine expression
* affine == constant : Again, the constant maybe a scalar or a matrix (see note)
* affine == affine : Affine expressions may be set equal to each other

Note: the left hand side of the equality is expected to have the same dimensions as the right hand side. For instance, a 4x3 affine expression can only be set equal to a constant, variable, or affine that is also 4x3. There is one exception that setting a variable or affine equal to a scalar creates an equality constraint that enforces all entries are equal to that scalar - this is known as broadcasting and is simply for convenience.

### Sum of Squares Expressions

	objective = sum_sq(expression) + 10*sumsq(x) # Create an objective

lsqpy handles objectives that are formed by summing the squares of the entries of an affine expression. As in the example above, a sumsq expression is formed by first creating a variable or affine expression then calling the function sumsq() on it. sumsq expressions can also be combined in two ways:
* The sum of two sumsq expressions is also a sumsq expression
* A sumsq expression can be multiplied by a positive scalar to produce a new sumsq expression

### Solving

	minimize(objective,[constraint])            # Solve the problem
	print(x.getValue())                         # Display the results

The 'minimize' function is called when it is time to solve the least-squares problem you have created. It takes as arguments an objective that is a sumsq expression, and a list of equality constraints to apply. The function will then attempt to solve. If a solution is found, the value of a variable can be obtained by calling the method getValue() on the variable.

There are two cases where 'minimize' will be unable to solve the problem. The first is when the system is over-determined ... The system may also be under-determined in which case ...
