"""
"""

import lsqpy.util.matutils as mutils
from ..constraint.eq_constraint import EqConstraint

import numpy as np
from scipy import sparse

""" Define function for checking if an object's type """
CONSTTYPES = (int,float,np.ndarray)
SCALARTYPES = (int,float)
def isValidConst(obj): return True if isinstance(obj,CONSTTYPES) else False
def isScalar(obj): return True if isinstance(obj,SCALARTYPES) else False

def constToAffine(obj,rows,cols):
	if isScalar(obj):
		new_affine = Affine(rows,cols)
		new_affine.coefs[Affine.CONST] = obj*sparse.csc_matrix(np.ones((rows,cols)))
	else:
		shape = (1,obj.shape[0]) if len(obj.shape) == 1 else obj.shape
		new_affine = Affine(shape[0],shape[1])
		new_affine.coefs[Affine.CONST] = sparse.csc_matrix(obj)
	return new_affine

class Affine:
	"""
		Represents a sent of affine expressions. We have one dictionary
		giving the coefficients for each element of each variable
	"""
	
	""" Change array priority so that we can overload operators correctly """
	__array_priority__ = 100
	
	""" Key for constant """
	CONST = 1

	def __init__(self,rows,cols):
		self.rows,self.cols = rows,cols
		self.coefs = {}
	
	def printme(self):
		for var in self.coefs:
			print(var)
			print(self.coefs[var].todense())

	""" Return basic information about this affine expression """
	def size(self): return (self.rows,self.cols)
	def getCoefs(self): return self.coefs
	def getVars(self): return [key for key in self.coefs]
	def getLinear(self,var_order):
		if Affine.CONST in var_order: var_order.remove(Affine.CONST)
		height = self.rows * self.cols
		return sparse.hstack([mutils.toColumn(self.coefs[var]) if var in self.coefs else sparse.csc_matrix((height,1)) for var in var_order])
	def getConst(self):
		if Affine.CONST in self.coefs: return self.coefs[Affine.CONST]
		else: return mutils.zeros(self.rows*self.cols,1)
	
	""" Functions to shape the affine expression """
	def T(self):
		pass
	def reshape(self,new_rows,new_cols):
		pass
	def slice(self,row_indices = [0],col_indices = [0]):
		""" Returns an affine expression of the subset of rows and cols specified """
		if len(row_indices) == 0 or len(col_indices) == 0:
			print('Warning: empty slice specified')
			return None
		if max(row_indices) >= self.rows or max(col_indices) >= self.cols:
			print('Warning: slice index exceeds dimension')
			return None
		num_rows,num_cols = len(row_indices),len(col_indices)
		new_affine = Affine(num_rows,num_cols)
		row_slicer = [[i] for i in row_indices]
		for key in self.coefs: new_affine.coefs[key] = self.coefs[key][row_slicer,col_indices]
		return new_affine

	""" Define the basic functions to combine affine expressions """
	def scale(self,val):
		new_affine = Affine(self.rows,self.cols)
		for key in self.coefs: new_affine.coefs[key] = val * self.coefs[key]
		return new_affine

	def lMulMat(self,mat):
		""" Perform mat*self """
		mat_shape = mutils.getShape(mat)
		if not mat_shape[1] == self.rows:
			print('Warning: matrix multiplication failed due to size mismatch')
			print(str(mat_shape) + ' * ' + str(self.size()))
			return None
		new_affine = Affine(mat_shape[0],self.cols)
		mat = sparse.csc_matrix(mat)
		for key in self.coefs: new_affine.coefs[key] = mat.dot(self.coefs[key])
		return new_affine
	def rMulMat(self,mat):
		""" Perform self*mat """
		mat_shape = mutils.getShape(mat)
		if not mat_shape[0] == self.cols:
			print('Warning: matrix multiplication failed due to size mismatch')
			print(str(self.size()) + ' * ' + str(mat_shape))
			return None
		new_affine = Affine(self.rows,mat_shape[1])
		mat = sparse.csc_matrix(mat)
		for key in self.coefs: new_affine.coefs[key] = self.coefs[key].dot(mat)
		return new_affine

	""" Overload the operators """
	def __eq__(self,other): return EqConstraint(self,other)
	def __neg__(self): return self.scale(-1)
	
	def __add__(self,other):
		if isValidConst(other): other = constToAffine(other,self.rows,self.cols)
		if not self.rows == other.rows or not self.cols == other.cols:
			print('Warning: matrix add/sub failed due to size mismatch')
			print(str(self.size()) + ' + ' + str(other.size()))
			return None
		new_affine = Affine(self.rows,self.cols)
		for key in self.coefs: new_affine.coefs[key] = self.coefs[key]
		for key in other.coefs:
			if key in self.coefs: new_affine.coefs[key] += other.coefs[key]
			else: new_affine.coefs[key] = other.coefs[key]
		return new_affine
	def __radd__(self,other): return self.__add__(other)
	def __sub__(self,other):
		if isValidConst(other): other = constToAffine(other,self.rows,self.cols)
		return self.__add__(other.__neg__())
	def __rsub__(self,other):
		if isValidConst(other): other = constToAffine(other,self.rows,self.cols)
		return self.__neg__().__add__(other)

	def __mul__(self,other):
		if isScalar(other): return self.scale(other)
		else: return self.rMulMat(other)
	def __rmul__(self,other):
		if isScalar(other): return self.scale(other)
		else: return self.lMulMat(other)