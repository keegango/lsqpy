from lsqpy.exprs.variable import Variable
import numpy as np

n = 3

print('scalar var')
z = Variable()
z.printme()

print('vector var')
y = Variable(n)
y.printme()

print('matrix var')
x = Variable(n,n)
x.printme()

print('scalar*variable')
(4*z).printme()
(4*y).printme()
(4*x).printme()

print('matrix*variable')
A = np.ones(n)
(A*y).printme()
(A*x).printme()

print('basic ops')
y2 = Variable(n)
x2 = Variable(n,n)

(y+y2).printme()
(x+x2).printme()
(A*(x+x2)).printme()

print('with constant')
(y+5).printme()
b = np.array([[1],[2],[7]])
(y+b).printme()

c = np.array(range(0,9)).reshape((3,3))
(x+c).printme()

if False:
	print('test large')
	w = Variable(10000000)