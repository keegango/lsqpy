from lsqpy.exprs.variable import Variable
import numpy as np

z = Variable()
x = Variable(3,3)

print('\nvariable*scalar')
(z*4).printme()

print('\nvariable*matrix')
b = np.array([[1,2,3]]).T
(x*b).printme()