"""
"""

from lsqpy.exprs.affine import *
from lsqpy.exprs.variable import *
import lsqpy.util.matutils as mutils
from scipy.sparse import linalg


class Problem:
	""" Formulation of a least squares problem """
	def __init__(self, normsq_expr, constraint_arr = []):
		self.eq_consts = constraint_arr
		self.normsq_expr = normsq_expr

	def collectVars(self):
		""" Make a list of all variables used """
		vars = []
		for eq_const in self.eq_consts: vars += eq_const.getVars()
		for affine in self.normsq_expr.sq_terms: vars += affine.getVars()
		vars = list(set(vars)) # Change to dictionary to avoid large list ops
		if Affine.CONST in vars: vars.remove(Affine.CONST)
		return vars

	def solve(self): 
		""" First get a list of all the variables and the number of new constraints we need """
		vars = self.collectVars()
		n = len(vars)
		num_new_constraints = self.normsq_expr.num_constraints()
		
		""" Create constraint matrices including those implicit constraints """

		constraint_mat = sparse.vstack(
			[aff.getLinear(vars) for aff in self.normsq_expr.sq_terms] +
            [eq_const.getLinear(vars) for eq_const in self.eq_consts])
		constraint_mat = sparse.hstack(
			[constraint_mat,-1*sparse.eye(constraint_mat.shape[0],num_new_constraints)]).tocsc()

		constraint_const = sparse.vstack(
			[-aff.getConst() for aff in self.normsq_expr.sq_terms] + 
			[-eq_const.getConst() for eq_const in self.eq_consts])

		""" Form the KKT_matrix to solve and solve it """
		total_constraints = constraint_const.shape[0]
		KKT_mat = mutils.cat([[mutils.gradMat(n,num_new_constraints),constraint_mat.T],
                              [constraint_mat,mutils.zeros(total_constraints,total_constraints)]])
		KKT_const = sparse.vstack([mutils.zeros(n+num_new_constraints,1),constraint_const])
		solution = linalg.spsolve(KKT_mat.tocsc(),KKT_const)
		
		""" Write results back to the correct variables """
		for i in range(len(vars)):
			var,row,col = vars[i]
			var.primal_value[row,col] = solution[i]
		self.val = solution[n:n+num_new_constraints].T.dot(solution[n:n+num_new_constraints])