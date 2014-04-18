"""
Class to represent normsq expressions that that are made up of a
sum of normsq(affine) terms possibly plus an affine
"""

from lsqpy.exprs.affine import Affine
import math

class SumSqExpr:
	def __init__(self, sq_terms=[], affine_term=Affine(1,1)):
		self.sq_terms = sq_terms
		self.affine_term = affine_term

	""" Get the number of constraints needed to convert the sq_terms to standard form """
	def num_constraints(self): return sum([aff.rows*aff.cols for aff in self.sq_terms])
		
	""" Addition is collecting the square terms and adding the affine component """
	def __add__(self,other):
		return SumSqExpr(self.sq_terms+other.sq_terms,self.affine_term+other.affine_term)
	def __radd__(self,other): return self.__add__(other)

	""" Multiplication is scaling each square term by sqrt(other) and the affine by other """
	def __mul__(self,other):
		if other < 0:
			print("Can only multiply a Norm Square Expression by a positive constant")
			return None
		new_sq_expr = SumSqExpr()
		const = math.sqrt(other)
		new_sq_expr.sq_terms = [const*aff for aff in self.sq_terms]
		new_sq_expr.affine_term = other*self.affine_term
		return new_sq_expr
	def __rmul__(self,other): return self.__mul__(other)

def sum_sq(affine_term):
	new_sumsq_expr = SumSqExpr()
	new_sumsq_expr.sq_terms = [affine_term]
	return new_sumsq_expr