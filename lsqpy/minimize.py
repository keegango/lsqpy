"""
The function to minimize a least squares problem
"""

from lsqpy.problem import *

def minimize(sq_term,constraint_arr = [],method='direct'):
	print('Begin minimization')
	if(method != 'direct' and method != 'iterative'):
		print("Bad solving method requested (should be 'direct' or 'iterative'")
		exit()
	p = Problem(sq_term,constraint_arr)
	if(method == 'direct'): p.minimize()
	else: p.minimizeLSMR()
	print('Solved, value = ' + str(p.val))

def solve(constraint_arr = []):
	print('Begin solve')
	p = Problem(None,constraint_arr)
	p.solve()
	print('Solved')