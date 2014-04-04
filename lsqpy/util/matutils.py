"""
Various utilities
"""
import numpy as np
from scipy import sparse

""" Because reshape is not implemented in current version of scipy.sparse """
def toColumn(a):
	c = a.tocoo()
	nrows, ncols = c.shape
	size = nrows * ncols
	flat_indices = ncols * c.row + c.col
	new_row, new_col = divmod(flat_indices, 1)
	return sparse.csc_matrix((c.data, (new_row, new_col)), shape=(size,1))

""" Get the shape of a matrix, handling when the matrix is 1-D """
def getShape(a):
	shape = a.shape
	if len(shape) == 1: shape = (1,shape[0])
	return shape

""" Create a sparse matrix of all zeros in the given format """
def zeros(rows,cols,sparse_type=sparse.csc_matrix):
	return sparse_type((rows,cols,))

""" Do a 2d cat of all the matrices. Argument should be list of list. """
def cat(mats):
	return sparse.vstack([sparse.hstack(row_of_mats) for row_of_mats in mats])

"""
Returns a diagonal matrix whose diagonal has n zeros followed by num_new_variable 2s
This is used in constructing the matrix to be solved for the lsq problem
"""
def gradMat(n,num_new_variables):
	total_size = n+num_new_variables
	return sparse.dia_matrix(
		([[0]*n+[2]*num_new_variables],[0]),
		shape=(total_size,total_size))
	