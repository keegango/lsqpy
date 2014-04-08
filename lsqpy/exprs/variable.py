"""
"""
from lsqpy.exprs.affine import Affine
from scipy import sparse

class Variable(Affine):
	INDEX = 0
	ID = 0
	
	def __init__(self,rows=1,cols=1,name=None):
		super().__init__(rows,cols)
		
		""" Give an ID which doubles as the start index for maxtrix stuffing """
		self.index = Variable.INDEX
		Variable.INDEX += cols*rows
		self.id = Variable.ID
		Variable.ID += 1
		self.name = name if name else 'Var'+str(self.id)
		self.primal_value = sparse.csc_matrix((rows,cols)).todense() # Replace with zeros for clarity
		for j in range(self.cols): self.vectors[j][(self,j)] = sparse.identity(rows)

	""" Return information about variable """
	def getValue(self): return self.primal_value
	def getName(self): return self.name
	def getColIndices(self,col):
		start = self.index+self.rows*col
		return list(range(start,start+self.rows))

	""" Re-override equality operator so that we can hash with it"""
	def __eq__(self,other):
		if not isinstance(other,Variable): return NotImplemented
		return id(self) == id(other)
	def __hash__(self): return id(self)