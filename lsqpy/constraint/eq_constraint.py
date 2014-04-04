"""
"""

class EqConstraint:
	""" Defines an equality constraint between affine expressions to check """
	
	def __init__(self,lhs,rhs):
		self.lhs = lhs
		self.rhs = rhs
		self.canonical = lhs-rhs

	def getVars(self): return [key for key in self.canonical.coefs]
	def getLinear(self,vars): return self.canonical.getLinear(vars)
	def getConst(self): return self.canonical.getConst()