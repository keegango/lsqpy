"""
The function to minimize a least squares problem
"""

from lsqpy.problem import *

def minimize(sq_term,constraint_arr = []):
	print('Begin minimization')
	p = Problem(sq_term,constraint_arr)
	p.minimize()
	print('Solved, value = ' + str(p.val))

def solve(constraint_arr = []):
	print('Begin solve')
	p = Problem(None,constraint_arr)
	p.solve()
	print('Solved')