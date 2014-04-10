from lsqpy.exprs.variable import Variable
import numpy as np

n = 3

print('\nscalar var')
z = Variable()
z.printme()

print('\nvector var')
y = Variable(n)
y.printme()

print('\nmatrix var')
x = Variable(n,n)
x.printme()

print('\nscalar*variable')
(4*z).printme()
(4*y).printme()
(4*x).printme()

print('\nmatrix*variable')
A = np.ones(n)
(A*y).printme()
(A*x).printme()

print('\nbasic ops')
y2 = Variable(n)
x2 = Variable(n,n)

(y-y2).printme()
(x-x2).printme()
(A*(x+x2)).printme()

print('\nwith constant')
(y+5).printme()
b = np.array([[1,2,7]]).T
(y+b).printme()

c = np.array(range(0,9)).reshape((3,3))
(x+c).printme()

print('\nslicing')
y[0:3:2].printme()
x[0:3:2,1:3].printme()
q = Variable(1,n)
(q[0:3:2] + q[1:]).printme()

if False:
	print('\ntest large')
	w = Variable(10000000)