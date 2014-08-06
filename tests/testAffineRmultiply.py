from lsqpy.exprs.variable import Variable
import numpy as np

z = Variable()
x = Variable(3,3)

print('\nvariable*scalar')
(z*4).printme()

print('\nvariable*vector')
b = np.array([[1,2,3]]).T
(x*b).printme()

print('\nvariable*matrix')
A = np.array(range(0,9)).reshape((3,3))
(x*A).printme()