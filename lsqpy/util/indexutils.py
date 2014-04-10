"""
Code to simplify indexing of matrices
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