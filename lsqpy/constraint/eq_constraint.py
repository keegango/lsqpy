"""
"""

class EqConstraint:
	""" Defines an equality constraint between affine expressions to check """
	
	def __init__(self,lhs,rhs):
		self.lhs = lhs
		self.rhs = rhs
		self.canonical = lhs-rhs

	def numConstraints(self):
		return self.canonical.rows * self.canonical.cols