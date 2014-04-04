"""
"""
from lsqpy.exprs.affine import Affine
from scipy import sparse

class Variable(Affine):
	
	def __init__(self,rows=1,cols=1):
		super().__init__(rows,cols)
		self.primal_value = sparse.csc_matrix((rows,cols)).todense()
		shape = (self.rows,self.cols)
		for i in range(self.rows):
			for j in range(self.cols):
				self.coefs[(self,i,j)] = sparse.csc_matrix(([1],([i],[j])),shape=shape)

	""" Return information about variable """
	def value(self): return self.primal_value

	""" Re-override equality operator so that we can hash with it"""
	def __eq__(self,other):
		if not isinstance(other,Variable): return NotImplemented
		return id(self) == id(other)
	def __hash__(self): return id(self)