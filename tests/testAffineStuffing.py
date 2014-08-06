from lsqpy.exprs.variable import Variable
import numpy as np

def test1():
	print('format vector')
	x = Variable(4)
	print(x.getLinear(4).todense())

def test2():
	print('format with multiple variables')
	x = Variable(4)
	y = Variable(4)
	(x-y).printme()
	print((x-y).getLinear(8).todense())

def test3():
	print('format matrix')
	x = Variable(4,3)
	print(x.getLinear(12).todense())

def test4():
	print('format affine')
	A = np.array(range(0,12)).reshape((3,4))
	b = np.array([[100],[200],[300]])
	x = Variable(4)
	y = Variable(3)
	aff = (A*x-y+b)
	print(aff.getLinear(7).todense())
	print(aff.getConst().todense())

test4()