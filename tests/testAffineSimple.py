from lsqpy.exprs.variable import Variable

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