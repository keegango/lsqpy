from lsqpy.exprs.variable import Variable
import numpy as np

z = Variable()
y = Variable(3)
x = Variable(3,3)

print('\nscalar*variable')
(4*z).printme()
(4*y).printme()
(4*x).printme()

print('\nmatrix*variable')
A = np.array(range(0,9)).reshape((3,3))
(A*y).printme()
(A*x).printme()