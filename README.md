#lsqpy

lsqpy is a library that makes it easy to formulate and solve least-squares optimization problems with linear equality constraints. With lsqpy, these types of problems can be created using a natural syntax for variables, constraints, and objectives that mirrors standard mathematical notation.

lsqpy's syntax and format are modelled on those of [cvxpy](https://github.com/cvxgrp/cvxpy "cvxpy"), a Python library that handles the larger class of convex optimization problems.

##Getting Started

Let's look at an example of what lsqpy can do. The files for this example are in [examples/simple_linreg](https://github.com/keegango/lsqpy/blob/master/examples/simple_linreg/ "linreg_example").

First we should visualize the data. In this example, the plotting is built into the data file so we can just run

	python data.py
	
which shows

![data](https://github.com/keegango/lsqpy/raw/master/images/linreg_data.png "linreg data")

The data is given as two lists: a list of x coordiantes, and a list of y coordinates. The plot above has points for each value of x paired with its corresponding value of y.

Since the data looks approximately linear, we can try fit a line to it. We can express our line as the function

	f(x) = slope*x_value + offset
	
If we knew the values for slope and offset, we would be able to predict what the value of y for any value of x just by plugging it into the function. This means the value of f(x) is our prediction of y should be given some value for x.

![results](https://github.com/keegango/lsqpy/raw/master/images/linreg_results.png "linreg results")

## Installing lsqpy

lsqpy relies on several other programs/packages.

### Python

[Python](https://www.python.org/downloads/,"Python download") is a widely used scripting language. Make sure you are using Python version 3 rather than 2.

### SciPy and NumPy

[SciPy](http://www.scipy.org/scipylib/download.html,"SciPy and Numpy Downloads") and [NumPy](http://www.scipy.org/scipylib/download.html,"SciPy and Numpy Downloads") are two Python libraries that provide support for many numeric tasks including formatting and computing maxtrix quantities. lsqpy makes use of these libraries to represent and manipulate vectors and matrices. Note you will need to make sure that you download the versions of SciPy and NumPy that match your version of python. You can check your version of Python by calling 'python -v' from your commandline.

Note: if you are running Windows (especially 64-bit) this [site](http://www.lfd.uci.edu/~gohlke/pythonlibs/,"Numpy for Windows") will have the packages you need.

### setuptools

[setuptools](https://pypi.python.org/pypi/setuptools,"setuptools") is a useful utility for installing Python modules. If you want to install lsqpy from source you will need this.

Once you have lsqpy cloned, go to that folder and run
	
	python setup.py install

### lsqpy

lsqpy is available for download ...

### matplotlib

One optional but extremely useful utility is matplotlib. It is a Python library that allows you to plot and view data. This library requires NumPy as well so be sure to install that first. Installing matplotlib may also require two other python libraries that do not come standard with Python: python-dateutil and pyparsing. These can be obatined using easy_install or pip.

On windows:

	cd < your python dir >
	cd Scripts
	easy_install python-dateutil
	easy_install pyparsing

## Full Specification

### Variables

	x = Variable(3) # Create a vector variable that has 3 rows and 1 columns
	y = Variable() # A scalar variable
	z = Variable(10,4) # A matrix variable that has 10 rows and 4 columns

Variables represent the quantities that we want to find. For example, a vector could represent holdings in a portfolio, or a matrix could represent the location of an object over time. lsqpy handles scalar, vector and matrix variables making it simple to create the appropriate variables for any problem.

### Affine Expressions

Affine expressions are built from certain combinations of variables, constants, and other affine expressions. These are:
* Two variables - added or subtracted
* A variable and a constant - added, subtracted or multiplied
* Two affine expressions - added or subracted
* An affine expression and a constant - added, subtracted or multiplied

Remember that all affine expressions, and variables as well, have dimensions and can only be combined with appropriately sized expressions.

### Equality Constraints

Equality constraints limit what values our variables can take on. For instance, a control problem might want to specify the position of an object at some moment in time. This would look like

	x[:,a_time] == a_position

The '==' operator will create equality constraints in the following situations:
* variable == constant
* variable == affine
* affine == constant
* affine == affine

### Sum of Squares Expressions
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
	print(x.getValue())                         # Display the results

The 'minimize' function is called when it is time to solve the least-squares problem you have created. It takes as arguments an objective that is a sumsq expression, and a list of equality constraints to apply. The function will then attempt to solve. If a solution is found, the value of a variable can be obtained by calling the method getValue() on the variable.

There are two cases where 'minimize' will be unable to solve the problem. The first is when the system is over-determined ... The system may also be under-determined in which case ...
