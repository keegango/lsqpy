"""
Test for norm square expressions
"""

from lsqpy.exprs.variable import Variable
from lsqpy.exprs.sumsq import sumsq

def printns(ns):
	print('has '+str(len(ns.sq_terms))+' sq terms')
	for aff in ns.sq_terms:
		aff.printme()
		print('******************************************')

z = Variable(2)
x = Variable(2)

nse = sumsq(z)+2*sumsq(x)
printns(nse)
print(nse.num_constraints()) # includes implicit constraints
