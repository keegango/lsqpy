from lsqpy.exprs.variable import Variable

y = Variable(3)

print('\nneg')
(-y).printme()

y2 = Variable(3)

print('\nadd')
(y+y2).printme()

print('\nsub')
(y-y2).printme()

x = Variable(3,3)
x2 = Variable(3,3)

print('\nneg')
(-x).printme()

print('\nadd')
(x+x2).printme()

print('\nsub')
(x-x2).printme()

exit(0)

print('\nslicing')
y[0:3:2].printme()
x[0:3:2,1:3].printme()
q = Variable(1,n)
(q[0:3:2] + q[1:]).printme()

print('\nsum')
sum(y).printme()
sum(x).printme()