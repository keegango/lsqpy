from lsqpy.exprs.variable import Variable
import numpy as np

z = Variable()
y = Variable(3)
x = Variable(3,3)

print('\nscalar variable add constant scalar')
(z+5).printme()

print('\nvector variable add constant scalar')
(y+5).printme()

print('\nvector variable add constant vector')
b = np.array([[1,2,3]]).T
(y+b).printme()

print('\nmatrix variable add constant matrix')
c = np.array(range(0,9)).reshape((3,3))
(x+c).printme()