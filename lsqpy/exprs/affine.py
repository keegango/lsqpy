"""
"""

import lsqpy.util.matutils as mutils
import lsqpy.util.indexutils as iutils
from lsqpy.constraint.eq_constraint import EqConstraint

import numpy as np
from scipy import sparse

""" Define function for checking if an object's type """
CONSTTYPES = (int,float,np.ndarray,sparse.coo.coo_matrix)
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

	def numElem(self): return self.rows*self.cols

	def isScalar(self): return True if self.rows == 1 and self.cols == 1 else False
	
	""" Access to data for problem solving """
	def indexVariables(self,included_vars,total_and_nnz):
		"""
			This method is called when problems are being initialized. It runs over all
			variables in this affine, and sets their index attribute which is their position
			into the KKT matrix. Updates the counts for the total number of variables and the
			number of non-zero entries in the constraint matrix
		"""
		# Store current counts locally, for readability
		num_vars, var_nnz, const_nnz = total_and_nnz
		for j in range(self.cols):
			for key in self.vectors[j]:
				# Update number of non-zero entries
				if key == Affine.CONST: const_nnz += self.vectors[j][key].nnz
				else: 
					var_nnz += self.vectors[j][key].nnz
					# Update set of variables
					var,col = key
					if not var in included_vars:
						num_vars = var.setIndex(num_vars)
						included_vars[var] = 0
		# Update counts to pass back
		total_and_nnz[0], total_and_nnz[1], total_and_nnz[2] = num_vars, var_nnz, const_nnz

	def getLinear(self,value_data,row_data,col_data,cur_row_and_entry):
		cur_row, cur_entry = cur_row_and_entry
		for j in range(self.cols):
			vector = self.vectors[j]
			for key in self.vectors[j]:
				if key == Affine.CONST: continue
				var,col = key
				""" Get offset of variable into table, then copy values """
				var_index_offset = var.getColIndices(col)
				coef_matrix = self.vectors[j][key].tocoo()
				for i in range(coef_matrix.nnz):
					value_data[cur_entry+i] = coef_matrix.data[i]
					row_data[cur_entry+i] = cur_row + coef_matrix.row[i]
					col_data[cur_entry+i] = var_index_offset + coef_matrix.col[i]
				cur_entry += coef_matrix.nnz
			cur_row += self.rows		
		cur_row_and_entry[0],cur_row_and_entry[1] = cur_row, cur_entry

	def getConst(self,value_data,row_data,cur_row_and_entry):
		cur_row, cur_entry = cur_row_and_entry
		for j in range(self.cols):
			if Affine.CONST in self.vectors[j]:
				coef_matrix = self.vectors[j][Affine.CONST].tocoo()
				for i in range(coef_matrix.nnz):
					value_data[cur_entry+i] = coef_matrix.data[i]
					row_data[cur_entry+i] = cur_row + coef_matrix.row[i]
				cur_entry += coef_matrix.nnz
			cur_row += self.rows
		cur_row_and_entry[0],cur_row_and_entry[1] = cur_row, cur_entry
	
	""" Functions to shape the affine expression """
	
	def T(self):
		"""
			Returns this affine transposed, probably runs slowly because of
			the need to copy entries and index. Avoid using if possible.
		"""
		new_affine = Affine(self.cols,self.rows)
		for j in range(self.cols):
			for key in self.vectors[j]:
				"""
					The rows of the matrix self.vectors[j][key] (representing
					one vector of the affine) are split across the columns of the
					new_affine.
				"""
				for i in range(self.rows):
					if not key in new_affine.vectors[i]:
						var = key[0]
						""" If not created already, add in a new matrix to fill """
						new_affine.vectors[i][key] = sparse.csc_matrix((self.cols,var.rows))
					new_affine.vectors[i][key][j,:] = self.vectors[j][key][i,:]
		return new_affine

	def reshape(self,new_rows,new_cols):
		if new_rows * new_cols != self.rows*self.cols:
			print("Number of elements does not match in reshape")
			return None
		new_affine = Affine(new_rows,new_cols)
		for j in range(self.cols):
			for key in self.vectors[j]:
				""" Copy rows to new affine mapping based on new size """
				for i in range(self.rows):
					elem_num = i*self.rows + j
					new_row_index, new_col_index = elem_num//new_rows, elem_num%new_cols
					if not key in new_affine.vectors[i]:
						var = key[0]
						new_affine.vectors[new_col_index][key] = sparse.csc_matrix((new_rows,var.rows))
					new_affine.vectors[new_col_index][key][new_row_index,:] = self.vectors[j][key][i,:]
		return new_affine
	
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
		"""
			Perform self*mat. This is done by individually evaluating each column
			of the new matrix as a weighted sum of the columns of self. This is
			not efficient and so it is recommended to avoid this if possible.
		"""
		mat_shape = mutils.getShape(mat)
		if not mat_shape[0] == self.cols:
			print('Warning: matrix multiplication failed due to size mismatch')
			print(str(self.size()) + ' * ' + str(mat_shape))
			return None
		new_affine = Affine(self.rows,mat_shape[1])
		for j in range(mat_shape[1]):
			new_affine_col = sum([mat[i,j]*self[:,i] for i in range(self.cols)])
			""" new_affine_col is always a vector of length self.rows """
			for key in new_affine_col[0]:
				new_affine[j][key] = new_affine_col[0][key]
		return new_affine

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