from lsqpy.affine import Affine
from lsqpy.variable import Variable
from lsqpy.problem import Problem
import numpy as np
from scipy import sparse


# Create some variables
x = Variable(1,2)
y = Variable(2)
z = Variable()
w = Variable(2)
H = Variable(2,2)

def printAffine(aff):
	for key in aff.coefs:
		if key == 1: print("AFFINE_CONST")
		else: print(key)
		print(aff.coefs[key].todense())
	print('------------------------------')

# Test basic operations
print('\nTESTING BASIC OPERATIONS')
y + z
y - z
printAffine(y + w)
printAffine(y - w)
printAffine(-y)
printAffine(2*y)

# Test matrix multiplication
print('\nTESTING OPS WITH NUMPY')
A = np.array([[2,3],[1,2]])
B = np.array([1,2])
C = sparse.csc_matrix(A)
printAffine(B+x)
printAffine(x+B)
printAffine(B-x)
printAffine(x-B)
printAffine(A * y)
printAffine(A*(y+w))
printAffine(A*H)
printAffine(H*A)

print('\nTESTING OPS WITH SCALAR')
printAffine(H+1)
printAffine(1+H)
printAffine(H-1)
printAffine(1-H)

# Test slice
print('\nTESTING SLICE')
v = Variable(3,3)
printAffine(A*v.slice([0,2],[0,2]))
v.slice([],[1,2])
v.slice([3],[1])

# Test formation of EqConstraints
print('\nTESTING EQCONST')
print(y == (w+0))
print((y+0) == w)
'''

A = sparse.csr_matrix([[0,1,2],[3,4,5],[6,7,8]])
Q = sparse.csr_matrix([[9],[10],[11]])
l = [A.tocoo(),Q.tocoo()]
for mat in l:
	print(type(mat))
print(sparse.hstack(l).todense())
'''
# Test simple system
p = Problem(w-np.array([[1],[2]]))
p.solve()
print(w.value())