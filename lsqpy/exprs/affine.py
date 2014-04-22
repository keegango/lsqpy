"""
"""

import lsqpy.util.matutils as mutils
import lsqpy.util.indexutils as iutils
from lsqpy.constraint.eq_constraint import EqConstraint

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
		for j in range(cols): new_affine.vectors[j][Affine.CONST] = obj*sparse.csc_matrix(np.ones((rows,1)))
	else:
		shape = mutils.getShape(obj)
		new_affine = Affine(shape[0],shape[1])
		for j in range(cols): new_affine.vectors[j][Affine.CONST] = sparse.csc_matrix(obj[:,j:j+1])
	return new_affine

class Affine:
	"""
		Represents a sent of affine expressions. We have one dictionary per column.
		The dictionary's keys are variables and the values are matrices.
	"""
	
	""" Change array priority so that we can overload operators correctly """
	__array_priority__ = 100
	
	""" Key for constant """
	CONST = 1

	def __init__(self,rows,cols):
		self.rows,self.cols = rows,cols
		self.vectors = [{} for _ in range(self.cols)]
	
	def printme(self):
		print('***************************')
		for j in range(self.cols):
			print('column '+str(j))
			for key in self.vectors[j]:
				if key == Affine.CONST: print('Constant')
				else:
					var,i = key
					print('Variable '+var.getName()+' column '+str(i))
				print(self.vectors[j][key].todense())
			print('-----------------------')
		print('***************************')

	""" Return basic information about this affine expression """
	def size(self): return (self.rows,self.cols)
	def isScalar(self): return True if self.rows == 1 and self.cols == 1 else False
	
	""" Access to data for problem solving """
	def getLinear(self,num_vars):
		mat_list = []
		for j in range(self.cols):
			mat = mutils.zeros(self.rows,num_vars,sparse.lil_matrix)
			for key in self.vectors[j]:
				if key == Affine.CONST: continue
				var,col = key
				mat[:,var.getColIndices(col)] = self.vectors[j][key]
			mat_list.append(mat)
		return sparse.vstack(mat_list).tocsc()
	def getConst(self):
		mat_list = []
		for j in range(self.cols):
			if Affine.CONST in self.vectors[j]: mat_list.append(self.vectors[j][Affine.CONST])
			else: mat_list.append(mutils.zeros(self.rows,1))
		return sparse.vstack(mat_list).tocsc()
	
	""" Functions to shape the affine expression """
	def T(self): pass # TODO
	def reshape(self,new_rows,new_cols): pass # TODO
	def broadcast(self,new_rows,new_cols):
		if not self.isScalar():
			print("Cannot broadcast a matrix")
			return None
		new_affine = Affine(new_rows,new_cols)
		for key in self.vectors[0]:
			new_mat = sparse.vstack([self.vectors[0][key] for _ in range(new_rows)])
			for j in range(new_cols): new_affine.vectors[j][key] = new_mat
		return new_affine
	""" For slicing """
	def __getitem__(self,indices):
		if self.cols == 1 and self.rows == 1: raise IndexError("Cannot index a scalar expression")
		if not isinstance(indices,tuple):
			if self.rows == 1: indices = (slice(0,1,1),indices)
			elif self.cols == 1: indices = (indices,slice(0,1,1))
			else: raise IndexError("Invalid index")
		indices = iutils.formatSlices(indices,(self.rows,self.cols))
		if indices[0].stop > self.rows or indices[1].stop > self.cols: raise IndexError("Invalid index")
		new_num_rows = iutils.numElem(indices[0],self.rows)
		new_num_cols = iutils.numElem(indices[1],self.cols)
		new_affine = Affine(new_num_rows,new_num_cols)
		new_col = 0
		for j in iutils.sliceToRange(indices[1],self.cols):
			for key in self.vectors[j]:
				new_affine.vectors[new_col][key] = self.vectors[j][key][indices[0],:]
			new_col += 1
		return new_affine

	""" Define the basic functions to combine affine expressions """
	def scale(self,val):
		new_affine = Affine(self.rows,self.cols)
		for j in range(self.cols):
			for key in self.vectors[j]: new_affine.vectors[j][key] = val * self.vectors[j][key]
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
		for j in range(self.cols):
			for key in self.vectors[j]: new_affine.vectors[j][key] = mat.dot(self.vectors[j][key])
		return new_affine
	def rMulMat(self,mat):
		""" Perform self*mat """
		pass # TODO

	""" Overload the rest of the operators """
	def __eq__(self,other): return EqConstraint(self,other)
	def __neg__(self): return self.scale(-1)
	
	def __add__(self,other):
		if isValidConst(other): other = constToAffine(other,self.rows,self.cols)
		
		""" If one of the expressions is a scalar, broadcast it """
		if self.isScalar() and not other.isScalar(): return self.broadcast(other.rows,other.cols)+other
		elif other.isScalar() and not self.isScalar(): return self+other.broadcast(self.rows,self.cols)
		
		if not self.rows == other.rows or not self.cols == other.cols:
			print('Warning: matrix add/sub failed due to size mismatch')
			print(str(self.size()) + ' + ' + str(other.size()))
			return None
		
		""" Copy new keys """
		new_affine = Affine(self.rows,self.cols)
		for j in range(self.cols):
			for key in self.vectors[j]: new_affine.vectors[j][key] = self.vectors[j][key]
			for key in other.vectors[j]:
				if key in self.vectors[j]:
					new_affine.vectors[j][key] = self.vectors[j][key] + other.vectors[j][key]
				else: new_affine.vectors[j][key] = other.vectors[j][key]
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
	
	""" Code to make affine iterable (for sum) """
	def __iter__(self):
		if self.rows == 1 and self.cols == 1:
			print('Scalar variables are not iterable')
			return None
		self.iter_index = 0
		return self
	def __next__(self):
		if self.iter_index >= self.rows*self.cols:
			del self.iter_index
			raise StopIteration
		else:
			self.iter_index += 1
			return self[(self.iter_index-1)%self.rows,(self.iter_index-1)//self.rows]