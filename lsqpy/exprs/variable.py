"""
"""
from lsqpy.exprs.affine import Affine
from scipy import sparse
import numpy as np

class Variable(Affine):
	INDEX = 0
	ID = 0
	VAR_LIST = []
	
	def __init__(self,rows=1,cols=1,name=None):
		super().__init__(rows,cols)
		
		""" Give an ID which doubles as the start index for maxtrix stuffing """
		self.index = Variable.INDEX
		Variable.INDEX += cols*rows
		
		self.id = Variable.ID
		Variable.ID += 1
		
		Variable.VAR_LIST.append(self)
		
		self.name = name if name else 'Var'+str(self.id)
		self.value = None
		for j in range(self.cols): self.vectors[j][(self,j)] = sparse.identity(rows).tocsc()

	""" Return information about variable """
	def getName(self): return self.name
	def getColIndices(self,col):
		start = self.index+self.rows*col
		return list(range(start,start+self.rows))
	def extractValues(self,solution):
		if solution is None: self.value = None
		else:
			self.value = sparse.csc_matrix((self.rows,self.cols)).todense()
			for j in range(self.cols):
				self.value[:,j:j+1] = solution[np.newaxis,self.getColIndices(j)].T

	""" Re-override equality operator so that we can hash with it"""
	def __eq__(self,other):
		if not isinstance(other,Variable): return NotImplemented
		return id(self) == id(other)
	def __hash__(self): return id(self)
