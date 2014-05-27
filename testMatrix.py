
from lsqpy import Matrix

a = Matrix([[1,2,3]])
b = Matrix([[6,5,4]])
print('a = ')
print(a)
print('b = ')
print(b)

# Run some tests
print('-------------------------------------')
print('ADD AND SUB')
print('-------------------------------------')
print('a+b')
print(a+b)
print('------------')
print('a-b')
print(a-b)
print('------------')
print('-a')
print(-a)
print('------------')
print('a+6')
print(a+6)
print('------------')
print('6+a')
print(6+a)
print('-------------------------------------')
print('TRANSPOSE')
print('-------------------------------------')
print(a.T)
print('-------------------------------------')
print('MUL AND DIV')
print('-------------------------------------')
print('a*b.T')
print(a*b.T)
print('------------')
print('a.T*b')
print(a.T*b)
print('------------')
print('6*a')
print(6*a)
print('------------')
print('a*6')
print(a*6)
print('------------')
print('a/2')
print(a/2)
print('-------------------------------------')
print('INDEXING')
print('-------------------------------------')
print('a[0]')
print(a[0])