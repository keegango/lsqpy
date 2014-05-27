"""
Code to simplify indexing of matrices, see last function in this file
"""

import math

def numElem(a_slice,num_elem):
	a_slice = formatSlice(a_slice,num_elem)
	return math.ceil((a_slice.stop - a_slice.start)/a_slice.step)

def sliceToRange(a_slice,num_elem):
	a_slice = formatSlice(a_slice,num_elem)
	return range(a_slice.start,a_slice.stop,a_slice.step)

def formatSlices(slices,num_elems):
	formated = []
	for i in range(len(slices)): formated.append(formatSlice(slices[i],num_elems[i]))
	return formated

def formatSlice(a_slice,num_elem):
	if isinstance(a_slice,int): return slice(a_slice,a_slice+1,1)
	start = 0 if a_slice.start is None else a_slice.start
	stop = num_elem if a_slice.stop is None else a_slice.stop
	step = 1 if a_slice.step == None else a_slice.step
	return slice(start,stop,step)
	
def wrapIndex(index,num_elem):
	""" To deal with negative indices """ # TODO USE 
	return index if index < 0 else index+num_elem
	
"""
The following is the main function to call to format indices.
The slicing syntax we use is as follows:
	mat[i] returns the (i+1)-th element of mat when mat is 1xn or nx1
	mat[x,y] where x and y can be any combination of scalar, list, or slice
		x selects the rows and y selects the cols
		if x/y is a scalar, selects a single row/col
		if x/y is a list, selects the rows/cols specified by x/y
		if x/y is a slice, selects those rows/cols
The function below is simply in charge of taking the form specifed above
	and mapping it into the numpy/scipy slicing format
Behavior is only tested for 2-d matrix
"""
def formatIndices(indices):
	modified_indices = []
	for i,index in enumerate(indices):
		if isinstance(index,(int)): modified_indices.append(slice(index,index+1))
		elif isinstance(index,(list)):
			if i == 0: modified_indices.append([[elem] for elem in index])
			else: modified_indices.append(index)
		elif isinstance(index,(slice)): modified_indices.append(index)
		else: print('FAILURE TO FORMAT INDICES: UNKNOWN TYPE OF INDEX')
	return tuple(modified_indices)