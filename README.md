#lsqpy

lsqpy is a library that makes it easy to formulate and solve least-squares optimization problems with linear equality constraints. With lsqpy, these types of problems can be created using a natural syntax for variables, constraints, and objectives that mirrors standard mathematical notation.

lsqpy's syntax and format are modelled on those of [cvxpy](https://github.com/cvxgrp/cvxpy "cvxpy"), a Python library that handles the larger class of convex optimization problems.

## Table of contents
* [Basic info](#basic-info "Basic info")
* [Tutorials](#tutorials "Tutorials")
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

	f(x) = slope*x + offset

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
	minimize(sum_sq(x_data*slope+offset-y_data))
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

Visually, the line does not seem to be a good fit for the data. It consistently overestimates points near the middle of the plot, and underestimates points near the edges of the plot. Now instead of using a line, let's try to fit a quadratic function to the data.

Our new function will be something of the form

	f(x) = a_0 + a_1*x + a_2*x^2

where a_0, a_1, and a_2 are the variables we are choosing.

To simplify writing this in code, we will create a matrix X that has 3 columns. The first column is all ones and represents the constant contribution. The second column is just x_data. The final column is x_data with its entries squared. To obtain f(x) for each point we just multiply X on the right by the vector

	[[a_0],
	 [a_1],
	 [a_2]]

which computes f(x) for each row. This process of generating new data from old is called augmenting.

Here is the [code](https://github.com/keegango/lsqpy/blob/master/examples/simple_linreg/simple_quadreg.py "quadreg code") that augments the data and solves the problem (again, plotting omitted)

	# Import lsqpy
	from lsqpy import Variable,sum_sq,minimize
	
	# Import the test data
	from data import x_data,y_data
	
	# Create a variable that holds the coefficients
	a = Variable(3)
	
	# We copy x_data but raise it to different powers
	# By treating these new columns as other predictors we can fit a quadratic
	# Here we import numpy to help format our data
	import numpy as np
	X = np.hstack([np.power(x_data,i) for i in range(3)])
	
	# Solve the problem
	minimize(sum_sq(X*a - y_data))

The code here is very much the same as the linear regression case. Running

	python simple_quadreg.py

will show the plot

![quad_results](https://github.com/keegango/lsqpy/raw/master/images/reg_quad.png "quadreg results")

Here, the fit looks much better as the function follows the curve of the data.

### Control

Another example of a least-squares problem is control, where we want to plan how something will move. In our example, we want our object to move from its starting location, reach a number of waypoints at specific times, and then return to rest at the start.

#### Data

The data consists a series of waypoints and some additional parameters. In this problem, time is represented by discrete intervals and our goal is to find a force to apply at each interval that will allow us to visit each of our waypoints at the specified time. In the data, T gives the number of time intervals, and h gives the length of each interval. In addition, we are also given the mass, and drag on the object which we will need to update our velocity at each interval.

#### Formulation

While force is the variable we want to determine, the position and velocity of the object are also unknown since they depend on the force. To solve the problem we will represent all three quantities as variables and use equality constraints to make sure values are consistent. These equality constraints are

p[t+1] = p[t] + h*v[t]
v[t+1] = v[t] + h/mass*f[t] - drag*v[t]

Finally, we need to decide on an objective. Here we will use the combination

	objective = sum_sq(f[t]) + mu*sum_sq(v[t]) for all t

This objective tells us that we want to minimize both the forces we apply as well as the speed of the object. mu is a constant that determines how much we care about the size of the forces versus the size of the velocity.

#### Solution

The [code](https://github.com/keegango/lsqpy/blob/master/examples/simple_control/simple_control.py "control code") is shown below (see the source for plotting).

	# Import lsqpy
	from lsqpy import Variable,sum_sq,minimize
	
	# Import numpy and plotting
	import numpy as np
	
	# Import the way points
	from data import waypoints,T,h,mass,drag
	
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
	# Add waypoint constraints evenly spaced
	zero_vector = np.array([[0,0]]).T
	for i in range(6): constraints.append(position[:,T*i//6] == waypoints[:,i:i+1])
	constraints.append(position[:,T-1] == zero_vector)
	# Add velocity constraints
	constraints.append(velocity[:,0] == zero_vector)
	constraints.append(velocity[:,T-1] == zero_vector)
	
	# Solve the problem
	mu = 1
	minimize(mu*sum_sq(velocity)+sum_sq(force),constraints)
	
The code roughly divides into three sections. We first create our variables: position, velocity, and force. We then create a list of our equality constraints that enforce consistency in our variables. Finally, we call solve. When you run the code with

	python simple_control.py

you should see a plot showing the trajectory of the object as well as the forces applied. For the code above the plot looks like

![control results](https://github.com/keegango/lsqpy/raw/master/images/control.png "control results")

In the plot above, the black arrows show the force applied to the object, the green arrows show the velocity, and the red line gives the actual position. Note how the position intersects each of the blue dots that represent the waypoints. 
At this point, you can play around with the value of mu to see how the weighting between force and velocity affects the motion of the object. You could even try include in the objective the sum of squares of the position as well. What will be the effect of that?

## User guide

### Variables

	x = Variable(3) # Create a vector variable that has 3 rows and 1 columns
	y = Variable() # A scalar variable
	z = Variable(10,4) # A matrix variable that has 10 rows and 4 columns

Variables represent the quantities that we want to find. For example, a vector could represent holdings in a portfolio, or a matrix could represent the location of an object over time. lsqpy handles scalar, vector and matrix variables making it simple to create the appropriate variables for any problem.

### Affine expressions

Affine expressions are built from certain combinations of variables, constants, and other affine expressions. These are:
* Two variables - added or subtracted
* A variable and a constant - added, subtracted or multiplied
* Two affine expressions - added or subtracted
* An affine expression and a constant - added, subtracted or multiplied

Remember that all affine expressions, and variables as well, have dimensions and can only be combined with appropriately sized expressions.

### Equality constraints

Equality constraints limit what values our variables can take on. For instance, a control problem might want to specify the position of an object at some moment in time. This would look like

	x[:,a_time] == a_position

The '==' operator will create equality constraints in the following situations:
* variable == constant
* variable == affine
* affine == constant
* affine == affine

### Sum of squares expressions
The objective of least-squares problems are sum of squares expressions, which are made by summing the square of each entry in one or more affine expressions. For example,

	x = Variable(4)
	sum_sq_expression = sum_sq(x)

In this case, we sum the squares of the entries of x, which turns out to be the length of x squared!

You can form sum of squares expression by:
* Calling sum_sq on an affine or variable
* Multiplying another sum of squares expression by a positive scalar
* Adding two sum of squares expressions together

For example,

	# 'A' is a constant matrix and x,y are variables.
	sum_sq_expression = sum_sq(A*x-y) + 100*sum_sq(x)

### Solving

	minimize(objective,[constraint])            # Solve the problem
	print(x.value)                              # Display the results

The 'minimize' function is called when it is time to solve the least-squares problem you have created. It takes as arguments an objective that is a sum of squares expression, and an optional list of equality constraints to apply. The function will then attempt to solve. If a solution is found, the value of a variable can be obtained as the value property of a variable as shown.

There are two cases where 'minimize' will be unable to solve the problem. The first is when the system is over-determined ... The system may also be under-determined in which case ...

## The math

TODO
