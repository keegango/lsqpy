"""
This Matrix class is used to wrap numpy and scipy so that users do not need
to manually import these. It also solves the problem of numpy/scipy array ordering
with the Affine class since now all operations will come through this class.

A sparse Matrix object is constructed from triplet format. It should be given 3 lists,
one for the row indices, one for the col indices, and one for the values
"""

import numpy as np
from scipy import sparse
import lsqpy.util.indexutils as iutils

# Define the types of scalars so we can automatically detect dimensionality of matrix
SCALARTYPES = (int,float)
# Define types of matrices we will allow for direct setting
MATRIXTYPES = (np.ndarray,sparse.coo_matrix)

class Matrix:
	def __init__(self,data,mat_type='full',shape=None):
		# First check that data is at least some kind of list or tuple
		if not isinstance(data,(list,tuple)) and not isinstance(data,MATRIXTYPES):
			raise RuntimeError('Data for Matrix must be a list or tuple')
		
		# Do a direct set if we are given a type in MATRIXTYPES
		if isinstance(data,MATRIXTYPES):
			self.data = data
		elif mat_type == 'full':
			# Check formatting, expects with a list of scalars or a lists of lists
			if len(data) == 0: raise RuntimeError('Cannot form Matrix without data')
			# Check for 1-D case, this because a n x 1 vector
			if isinstance(data[0],SCALARTYPES): self.data = np.array(data)[:,np.newaxis]
			else:
				self.data = np.array(data)
				if len(self.data.shape) > 2: raise RuntimeError('Data for Matrix must only be 2d')
		elif(mat_type == 'sparse'):
			if not shape: raise RuntimeError('A sparse Matrix must be given a shape in the form (rows,cols)')
			if len(data) != 3: raise RuntimeError('A sparse Matrix expects a list containing 3 lists for data')
			self.data = sparse.coo_matrix((data[2],(data[0],data[1])),shape=shape)
		else: raise RuntimeError('Matrix type must either be full or sparse')
		self.shape = self.data.shape
		self.mat_type = mat_type
	
	"""
	Here we define the list of operators supposed by Matrix. There are only a few case that need to be
	taken care of. These are:
		scalar [+,-,*] Matrix or Matrix / scalar
		Matrix [+,-,*] Matrix
		Matrix [+,-,*] Affine or Affine [+,-,*] Matrix
	The last case is handled by Affine and so we just need to ensure no result is returned.
	"""
	def __neg__(self): return Matrix(-1*self.data,self.mat_type)
	def __add__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data+other,self.mat_type)
		if isinstance(other,Matrix): return Matrix(self.data+other.data,self.mat_type)
		raise NotImplementedError
	def __radd__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data+other,self.mat_type)
		raise NotImplementedError
	def __sub__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data-other,self.mat_type)
		if isinstance(other,Matrix): return Matrix(self.data-other.data,self.mat_type)
		raise NotImplementedError
	def __rsub__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(other-self.data,self.mat_type)
		raise NotImplementedError
	def __mul__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data*other,self.mat_type)
		if isinstance(other,Matrix): return Matrix(self.data.dot(other.data),self.mat_type)
		raise NotImplementedError
	def __rmul__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data*other,self.mat_type)
		raise NotImplementedError
	def __div__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data/other,self.mat_type)
		raise NotImplementedError
	def __truediv__(self,other):
		if isinstance(other,SCALARTYPES): return Matrix(self.data/other,self.mat_type)
		raise NotImplementedError
	
	"""
	Define __str__ for printing
	"""
	def __str__(self): return self.data.__str__()
	
	"""
	Use index values to slice matrix
	"""
	def __getitem__(self,indices):
		modified_indices = iutils.formatIndices(indices)
		return Matrix(self.data.__getitem__(modified_indices))
	def __setitem__(self,indices,value):
		print('set item called')
		if not isinstance(value,SCALARTYPES) and not isinstance(value,(Matrix)):
			raise RuntimeError('Matrix can only be set with a scalar or a Matrix')
		modified_indices = iutils.formatIndices(indices)
		if isinstance(value,SCALARTYPES): self.data.__setitem__(modified_indices,value)
		else: self.data.__setitem__(modified_indices,value.data)
	
	"""
	Other useful elementwise operations
	"""
	def power(self,n):
		""" Raise each element of self to the nth power """
		return Matrix(np.power(self.data,n),self.mat_type)

	"""
	Transpose
	"""
	@property
	def T(self): return Matrix(self.data.T,self.mat_type)
	
	"""
	Reshape
	"""
	def reshape(self,new_rows,new_cols):
		if new_rows*new_cols != self.shape[0]*self.shape[1]:
			raise RuntimeError('reshape requires that the total number of elements to remains constant')
		return Matrix(self.data.reshape(new_rows,new_cols))
	
	"""
	Define a number of class methods that create common matricies
	"""
	def zeros(rows,cols,mat_type='full'):
		new_shape = (rows,cols)
		if mat_type == 'full': return Matrix(np.zeros(new_shape),mat_type)
		elif mat_type == 'sparse': return Matrix(sparse.coo_matrix(new_shape),mat_type)
		else: raise RuntimeError('Matrix type must either be full or sparse')

	def eye(rows,cols,mat_type='full'):
		if mat_type == 'full': return Matrix(np.eye(rows,cols),mat_type)
		elif mat_type == 'sparse':
			raise NotImplementedError
		else: raise RuntimeError('Matrix type must either be full or sparse')
		
	"""
	Stacking operations
	"""
	def hcat(matrix_list): return Matrix(np.hstack([mat.data for mat in matrix_list]),'full')
	def vcat(matrix_list): return Matrix(np.vstack([mat.data for mat in matrix_list]),'full')