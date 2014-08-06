"""
Test for norm square expressions
"""

from lsqpy.exprs.variable import Variable
from lsqpy.exprs.sum_squares import sum_squares

def printns(ns):
	print('has '+str(len(ns.sq_terms))+' sq terms')
	for aff in ns.sq_terms:
		aff.printme()
		print('******************************************')

z = Variable(2)
x = Variable(2)

nse = sum_squares(z)+2*sum_squares(x)
printns(nse)
print(nse.num_constraints()) # includes implicit constraints
