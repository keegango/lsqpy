"""
"""
from lsqpy.exprs.affine import Affine
from scipy import sparse
import numpy as np

class Variable(Affine):
	ID = 0
	VAR_LIST = []
	
	def __init__(self,rows=1,cols=1,name=None):
		super().__init__(rows,cols)
		
		self.id = Variable.ID
		Variable.ID += 1
		
		Variable.VAR_LIST.append(self)
		
		self.name = name if name else 'Var'+str(self.id)
		self.value = None
		for j in range(self.cols): self.vectors[j][(self,j)] = sparse.identity(rows).tocsc()

	""" Return information about variable """
	def getName(self): return self.name
	def getColIndices(self,col): return self.index+self.rows*col
	def setIndex(self,index):
		self.index = index
		return index + self.cols*self.rows
	def extractValues(self,solution):
		if solution is None: self.value = None
		else:
			self.value = sparse.csc_matrix((self.rows,self.cols)).todense()
			for j in range(self.cols):
				start_col = self.getColIndices(j)
				self.value[:,j:j+1] = solution[np.newaxis,start_col:(start_col+self.rows)].T
			self.value = np.array(self.value)

	""" Re-override equality operator so that we can hash with it"""
	def __eq__(self,other):
		if not isinstance(other,Variable): return NotImplemented
		return id(self) == id(other)
	def __hash__(self): return id(self)
