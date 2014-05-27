"""
This Matrix class is used to wrap numpy and scipy so that users do not need
to manually import these. It also solves the problem of numpy/scipy array ordering
with the Affine class since now all operations will come through this class.

A sparse Matrix object is constructed from triplet format. It should be given 3 lists,
one for the row indices, one for the col indices, and one for the values
"""

import numpy as np
from scipy import sparse

# Define the types of scalars so we can automatically detect dimensionality of matrix
SCALARTYPES = (int,float)
# Define types of matrices we will allow for direct setting
MATRIXTYPES = (np.ndarray,sparse.coo_matrix)

class Matrix:
	def __init__(self,data,type='full',shape=None):
		# First check that data is at least some kind of list or tuple
		if not isinstance(data,(list,tuple)): raise RuntimeError('Data for Matrix must be a list or tuple')
		
		# Do a direct set if we are given a type in MATRIXTYPES
		if isinstance(data,MATRIXTYPES):
			self.data = data
		elif type == 'full':
			# Check formatting, expects with a list of scalars or a lists of lists
			if len(data) == 0: raise RuntimeError('Cannot form Matrix without data')
			# Check for 1-D case, this because a n x 1 vector
			if isinstance(data[0],SCALARTYPES): self.data = np.array(data)[:,np.newaxis]
			else:
				self.data = np.array(data)
				if len(self.data.shape) > 2: raise RuntimeError('Data for Matrix must only be 2d')
		elif(type == 'sparse'):
			if not shape: raise RuntimeError('A sparse Matrix must be given a shape in the form (rows,cols)')
			if len(data) != 3: raise RuntimeError('A sparse Matrix expects a list containing 3 lists for data')
			self.data = sparse.coo_matrix((data[2],(data[0],data[1])),shape=shape)
		else: raise RuntimeError('Matrix type must either be full or sparse')
		self.shape = self.data.shape
		self.type = type
	
	"""
	Here we define the list of operators supposed by Matrix. There are only a few case that need to be
	taken care of. These are:
		scalar [+,-,*] Matrix or Matrix / scalar
		Matrix [+,-,*] Matrix
		Matrix [+,-,*] Affine or Affine [+,-,*] Matrix
	The last case is handled by Affine and so we just need to ensure no result is returned.
	"""
	def __neg__(self): return Matrix(-1*self.data,self.type)
	def __add__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data+other,self.type)
		if isinstance(other,Matrix): return Matrix(self.data+other.data,self.type)
		raise NotImplementedError
	def __radd__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data+other,self.type)
		raise NotImplementedError
	def __sub__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data-other,self.type)
		if isinstance(other,Matrix): return Matrix(self.data-other.data,self.type)
		raise NotImplementedError
	def __rsub__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(other-self.data,self.type)
		raise NotImplementedError
	def __mul__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data*other,self.type)
		if isinstance(other,Matrix): return Matrix(self.data.dot(other.data),self.type)
		raise NotImplementedError
	def __rmul__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data*other,self.type)
		raise NotImplementedError
	def __rdiv__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data/other,self.type)
		raise NotImplementedError
	
	"""
	Define __str__ for printing
	"""
	def __str__(self): return self.data.__str__()
	
	"""
	Use index values to slice matrix
	"""
	def __getitem__(self,a,b):
		print(a)
		print(b)
	@property
	def T(self): return Matrix(self.data.T,self.type)