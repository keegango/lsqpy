"""
The function to minimize a least squares problem
"""

from lsqpy.problem import *

def minimize(sq_term,constraint_arr = [],solver_type='direct'):
	print('Begin minimization')
	if(solver_type != 'direct' and solver_type != 'iterative'):
		print("Invalid solver type requested (should be 'direct' or 'iterative'")
		exit()
	p = Problem(sq_term,constraint_arr)
	if(solver_type == 'direct'): p.minimize()
	else: p.minimizeLSMR()
	print('Solved, value = ' + str(p.val))

def solve(constraint_arr = []):
	print('Begin solve')
	p = Problem(None,constraint_arr)
	p.solve()
	print('Solved')