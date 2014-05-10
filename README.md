#lsqpy

lsqpy is a library that makes it easy to formulate and solve least-squares optimization problems with linear equality constraints. With lsqpy, these types of problems can be created using a natural syntax for variables, constraints, and objectives that mirrors standard mathematical notation.

lsqpy's syntax and format are modelled on those of [cvxpy](https://github.com/cvxgrp/cvxpy "cvxpy"), a Python library that handles the larger class of convex optimization problems.

## Table of contents
* [Basic info](#basic-info "Basic info")
* [Tutorials](#tutorials "Tutorials")
	* [Regression](#regression "Regression")
	* [Control](#control "Control")
* [Installing lsqpy](#installing-lsqpy "Installing lsqpy")
* [User guide](#user-guide "User guide")
* [The math](#the-math "The math")

## Basic info

### Installing lsqpy

lsqpy relies on several other programs/packages.

#### Python

[Python](https://www.python.org/downloads/,"Python download") is a widely used scripting language. Make sure you are using Python version 3 rather than 2.

#### SciPy and NumPy

[SciPy](http://www.scipy.org/scipylib/download.html,"SciPy and Numpy Downloads") and [NumPy](http://www.scipy.org/scipylib/download.html,"SciPy and Numpy Downloads") are two Python libraries that provide support for many numeric tasks including formatting and computing matrix quantities. lsqpy makes use of these libraries to represent and manipulate vectors and matrices. Note you will need to make sure that you download the versions of SciPy and NumPy that match your version of python. You can check your version of Python by calling 'python -v' from your command-line.

Note: if you are running Windows (especially 64-bit) this [site](http://www.lfd.uci.edu/~gohlke/pythonlibs/,"Numpy for Windows") will have the packages you need.

#### setuptools

[setuptools](https://pypi.python.org/pypi/setuptools,"setuptools") is a useful utility for installing Python modules. If you want to install lsqpy from source you will need this.

#### lsqpy

Currently, lsqpy is hosted on GitHub as a public repository. To install it, first clone the repository with the command

	git clone https://github.com/keegango/lsqpy.git

Once you have lsqpy cloned, go to that folder and run
	
	python setup.py install

#### matplotlib

One optional but extremely useful utility is matplotlib. It is a Python library that allows you to plot and view data among other things. This library requires NumPy as well so be sure to install that first. Installing matplotlib may also require two other Python libraries that do not come standard with Python: python-dateutil and pyparsing. These can be obtained using easy_install or pip.

On windows:

	cd < your python dir >
	cd Scripts
	easy_install python-dateutil
	easy_install pyparsing

## Tutorials

### Regression

This is an example of using lsqpy for regression - the problem of trying to fit a function to some data.

The files for this example are in [examples/simple_linreg](https://github.com/keegango/lsqpy/blob/master/examples/simple_linreg/ "linreg_example").

#### Data

In this problem, we are given n points, represented by two n-by-1 vectors: x_data and y_data. The x and y coordinates of the ith point are given by the ith entries of x_data and y_data respectively.

We should first visualize the [data](https://github.com/keegango/lsqpy/blob/master/examples/simple_linreg/data.py "linreg data"). In this example, the plotting is built into the data file so we can just run

	python data.py
	
which shows

![data](https://github.com/keegango/lsqpy/raw/master/images/reg_data.png "linreg data")

#### Linear regression

We will first try to fit a line to the data. A general function for a line is:

	f(x) = offset + slope*x

where slope and offset are scalar quantities that we pick to determine the line.

We would like our data points to be "close" the line given by the slope and offset we pick. To define "close", we measure a residual defined as

	residual(x,y) = f(x) - y

for each point (x,y) in our data. Note that when the residual is small in magnitude the value of f(x) is close to y which means the line passes near the point. To account for the residual across multiple points we sum the squares of the residuals to obtain

	total_residual_sq = sum of square(residual(x,y)) for each point (x,y)

The values we want for slope and offset will be the ones that minimize total_residual_sq.

We can now use lsqpy to solve this problem. The [code](https://github.com/keegango/lsqpy/blob/master/examples/simple_linreg/simple_linreg.py "linreg code") for this example is shown below (with the plotting omitted):

	# Import lsqpy
	from lsqpy import Variable,sum_sq,minimize
	
	# Import the test data
	from data import x_data,y_data
	
	# Solve the problem, and print the result
	slope = Variable()
	offset = Variable()
	minimize(sum_squares(offset + x_data*slope - y_data))
	print('slope = '+str(slope.value[0,0])+', offset = '+ str(offset.value[0,0]))

The first section includes lsqpy for use, and the second makes the data accessible. The third section contains the actual work. We first declare two Variables, one for each of the quantities we want to determine. Then we call the lsqpy function 'minimize' and pass in our expression to minimize. Calling minimize both finds the minimum value of the expression and sets all variables in the problem with values that achieve this minimum. With the values set, all we have to do is print the results.

You can run the above code in your console with

	python simple_linreg.py

This will print

	Begin minimization
	Solved, value = 102.042139506
	slope = 0.407196109544, offset = 0.238777593277

and also display the a plot of the line we found.

![lin_results](https://github.com/keegango/lsqpy/raw/master/images/reg_lin.png "linreg results")

#### Quadratic regression

Now instead of using a line, let's try to fit a quadratic function to the data.

Our new function will be something of the form

	f(x) = offset + slope*x + quadratic*x^2

which is similar to the linear function we used previously. The only difference is that we have introduced an x^2 term with a new Variable coefficient. Along with offset and slope, quadratic is a Variable that we wish to determine.

Here is the [code](https://github.com/keegango/lsqpy/blob/master/examples/simple_linreg/simple_quadreg.py "quadreg code") that solves the problem (again, with plotting omitted)

	# Import lsqpy
	from lsqpy import Variable,sum_squares,minimize
	
	# Import the test data
	from data import x_data,y_data
	
	# Create variables that holds the coefficients
	quadratic = Variable()
	slope = Variable()
	offset = Variable()
	
	# We copy x_data but square the entries
	import numpy as np
	x_squared = np.power(x_data,2)
	
	# Solve the problem
	minimize(sum_squares(offset + x_data*slope + x_squared*quadratic - y_data))

The code here is very much the same as the linear regression case. Running

	python simple_quadreg.py

will show the plot

![quad_results](https://github.com/keegango/lsqpy/raw/master/images/reg_quad.png "quadreg results")

### Control

Another example of a least-squares problem is control, where we want to plan how something will move. In our example, we want to determine the forces that will move our object to a goal position.

#### Formulation

There are 3 unknown quantities in the problem: the force applied, the velocity of the object, and the position of the object. To solve this problem, we will break up time into T points, each h seconds apart. The values of our variables must then satisfy

	p[t+1] = p[t] + h*v[t]
	v[t+1] = v[t] + h/mass*f[t] - drag*v[t]

where p[t], v[t], and f[t] are the position, velocity, and force respectively at time t. This model is only an approximation of the real dynamics of moving objects, but when h is small this model is reasonable accurate.

Finally, we need to decide on an objective. Here we will use the combination

	objective = mu*sum_squares(v[t]) + sum_squares(f[t]) for all t

This objective tells us that we want to minimize both the forces we apply as well as the speed of the object. mu is a constant that determines how much we care about the size of the forces versus the size of the velocity.

#### Solution

The [code](https://github.com/keegango/lsqpy/blob/master/examples/simple_control/simple_control.py "control code") is shown below.

	# Import lsqpy
	from lsqpy import Variable, sum_sq, minimize

	# Import the way points
	from data import initial_velocity, final_position, T, h, mass, drag
	
	# Declare the variables we need
	position = Variable(2,T)
	velocity = Variable(2,T)
	force = Variable(2,T-1)
	
	# Create the list of constraints on our variables
	constraints = []
	for i in range(T-1):
		constraints.append(position[:,i+1] == position[:,i] + h * velocity[:,i])
	for i in range(T-1):
		constraints.append(velocity[:,i+1] == velocity[:,i] + h/mass * force[:,i] - drag*velocity[:,i])
		
	# Add position constraints
	constraints.append(position[:,0] == 0)
	constraints.append(position[:,T-1] == final_position)
	
	# Add velocity constraints
	constraints.append(velocity[:,0] == initial_velocity)
	constraints.append(velocity[:,T-1] == 0)
	
	# Solve the problem
	mu = 1
	minimize(mu*sum_squares(velocity)+sum_squares(force),constraints)
	
The code roughly divides into three sections. We first create our variables: position, velocity, and force. We then create a list of our equality constraints that enforce consistency in our variables. Finally, we call solve. When you run the code with

	python simple_control.py

you should see this plot

![control results](https://github.com/keegango/lsqpy/raw/master/images/control.png "control results")

The black arrows show the force applied to the object, and the red line gives the actual position.

At this point, you can play around with the value of mu to see how the weighting between force and velocity affects the motion of the object. You could even try include in the objective the sum of squares of the position as well. What effect will this have?

## User guide

### Variables

Variables represent the quantities that we want to find. lsqpy handles scalar, vector and matrix variables as shown below.

	x = Variable() # A scalar variable
	y = Variable(3) # Create a vector variable with 3 rows and 1 columns
	z = Variable(10,4) # A matrix variable that has 10 rows and 4 columns

Variables are objects, not numeric quantities. Their value is set by calling either minimize or solve. After these functions are called, the value of a variable can be obtained through its value attribute. For example,

	x = Variable(10)
	... # Add some constraints
	minimize(x,constraints)
	
	# Print the numeric value of x that minimizes the above problem
	print(x.value) 

### Affine expressions

Affine expressions are made from variables, constants, and other affine expressions using the operations +, -, and *. There are a few rules about what can be combined for each operator.

For addition and subraction, the two expressions being combined must either have the same dimensions or one of the two must be a scalar. When one expression is a scalar, it is added to each entry of the other expression. For example,

	x = Variable(3)
	y = Variable(2)
	z = Variable(3)
	
	x + z # Ok
	x + y # Fails
	z - x # Ok
	
	w = Variable() # A scalar variable
	x + w # Ok
	y + 1 # Ok

On the other hand, multiplication will only work between an affine expression and a constant. If either expression is a scalar, the multiplication will work regardless of the size of the other expression.

	x = Variable(3)
	y = Variable()
	
	x*y # Fails, one must be a constant
	5*x # Ok
	y*np.array([[1,2,3]])

However, if both expressions are vectors or matrices then their sizes must match in the usual matrix/vector multiplication sense. This means we can only perform A*B if A is m-by-n and B is n-by-p.

	x = Variable(4) # A 4-by-1 matrix
	A = np.array([[1,2,3,4]]) # A 1-by-4 matrix
	B = np.array([[1,2,3]]) # A 1-by-3 matrix
	
	B*x # Fails
	A*x # Ok

Finally, a few common operations have been created for affine to make formulating your problem simpler.

	x = Variable(10)
	
	# A scalar affine expression who value is the sum of the entries of x
	sum(x)
	
	# Indexing
	x[0] # Indexing to get the first entry of x
	x[0:4] # Index the first 3 entries of x
	y = Variable(3,3)
	y[2,1:3] # Get the 3rd row of y, and columns 2 and 3, remember python is zero-indexed

### Equality constraints

The '==' operator creates equality constraints between two affine expressions.

	x = Variable()
	y = Variable()
	x == y + 2 # An equality constraint

Similar to addition or subtraction, an equality constraint can only be created if two expressions have equal dimensions or if one expression is a scalar.

	x = Variable(3,10)
	y = Variable(4,10)
	z = Variable() # A scalar variable
	
	x == y # Fails
	x == y[0:3,:] # Ok, we dropped the last row from y making it 3-by-10
	x == z # Ok

### Sum of squares expressions
Sum of squares expressions are created by summing the square of each entry in an affine expression. If you have an affine expression, a sum of sqaures expression can be created by calling the function sum_squares as shown below.

	x = Variable(4)
	sum_sq_expression = sum_squares(x)

Sum of squares expressions can also be created by combining two other sum of squares expressions with +, or by multiplying a sum of squares expression by a non-negative scalar.

	y = Variable(18)
	z = Variable(20)
	
	sum_squares(y) + sum_squares(z) # Ok
	10*sum_squares(z) # Ok
	-1*sum_squares(z) # Fails

### Solving

	minimize(objective,[constraint])            # Solve the problem
	print(x.value)                              # Display the results

The 'minimize' function is called when it is time to solve the least-squares problem you have created. It takes as arguments an objective that is a sum of squares expression, and an optional list of equality constraints to apply. The function will then attempt to solve. If a solution is found, the value of a variable can be obtained as the value property of a variable as shown.

There are two cases where 'minimize' will be unable to solve the problem. The first is when the system is over-determined ... The system may also be under-determined in which case ...

## The math

TODO
