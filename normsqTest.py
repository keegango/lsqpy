"""
Test for norm square expressions
"""

from lsqpy.exprs.variable import Variable
from lsqpy.exprs.normsq import normsq

def printAffine(aff):
	for key in aff.coefs:
		print("AFFINE_CONST") if key == 1 else print(key)
		print(aff.coefs[key].todense())
	print('------------------------------')

def printns(ns):
	print('has '+str(len(ns.sq_terms))+' sq terms')
	for aff in ns.sq_terms:
		printAffine(aff)
		print('****************************')

z = Variable(2)
x = Variable(2)

nse = normsq(z)+2*normsq(x)
printns(nse)
print(nse.num_constraints())
