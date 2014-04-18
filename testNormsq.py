"""
Test for norm square expressions
"""

from lsqpy.exprs.variable import Variable
from lsqpy.exprs.sum_sq import sum_sq

def printns(ns):
	print('has '+str(len(ns.sq_terms))+' sq terms')
	for aff in ns.sq_terms:
		aff.printme()
		print('******************************************')

z = Variable(2)
x = Variable(2)

nse = sum_sq(z)+2*sum_sq(x)
printns(nse)
print(nse.num_constraints()) # includes implicit constraints
