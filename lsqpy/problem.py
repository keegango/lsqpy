"""
"""

from lsqpy.exprs.affine import *
from lsqpy.exprs.variable import *
import lsqpy.util.matutils as mutils
from scipy.sparse import linalg

class Problem:
	""" Formulation of a least squares problem """
	def __init__(self, sumsq_expr, constraint_arr = []):
		self.eq_consts = constraint_arr
		self.sumsq_expr = sumsq_expr
		self.included_vars = {}
		self.total_vars_and_nnz = self.collectVars(self.included_vars)

	"""
		Collect some information:
			1. The variables used in this problem (included_vars)
			2. The total number of (scalar) variables, stored as total_and_nnz[0]
			3. The number of non-zero entries that will be put in the constraint matrix,
				this allows for preallocation (10x speedup), stored as total_and_nnz[1]
			4. The number of non-zero entries in the constant part of the constraint matrix,
				stored as total_and_nnz[2]
	"""
	def collectVars(self,included_vars):
		total_vars_and_nnz = [0,0,0]
		if self.sumsq_expr:
			for aff in self.sumsq_expr.sq_terms: aff.indexVariables(included_vars,total_vars_and_nnz)
		for eq_const in self.eq_consts: n = eq_const.canonical.indexVariables(included_vars,total_vars_and_nnz)
		return total_vars_and_nnz
		
	def createConstraintMat(self,total_constraints,total_vars_and_nnz):
		"""
			Lists we will use to store the non-zero entries of the constraint matrices.
			Preallocation helps a lot with speed
		"""
		#print('begin make mat')
		num_entries = total_vars_and_nnz[1]
		value_data = [0]*num_entries
		row_data = [0]*num_entries
		col_data = [0]*num_entries
		
		"""
			Fill in the lists by iterating over all the expressions used in the problem
			The 2 element array cur_row_and_entry keep track of the next row and entry of data
			to be filled, it is updated inside the getLinear calls
		"""
		cur_row_and_entry = [0,0]
		if(self.sumsq_expr):
			for aff in self.sumsq_expr.sq_terms:
				aff.getLinear(value_data,row_data,col_data,cur_row_and_entry)
		for eq_const in self.eq_consts:
			eq_const.canonical.getLinear(value_data,row_data,col_data,cur_row_and_entry)
		shape = (total_constraints,total_vars_and_nnz[0])
		return sparse.coo_matrix((value_data,(row_data,col_data)),shape)
	
	# Create a matrix(vector) that contains the constant terms from each equality constraint
	def createConstMat(self,total_constraints,total_vars_and_nnz):
		""" Allocate the right number of entries for the constant expression """
		num_entries = total_vars_and_nnz[2]
		value_data = [0]*num_entries
		row_data = [0]*num_entries
		cur_row_and_entry = [0,0]
		if self.sumsq_expr:
			for aff in self.sumsq_expr.sq_terms: aff.getConst(value_data,row_data,cur_row_and_entry)
		for eq_const in self.eq_consts: eq_const.canonical.getConst(value_data,row_data,cur_row_and_entry)
		shape = (total_constraints,1)
		return -sparse.coo_matrix((value_data,(row_data,[0]*num_entries)),shape)

	def minimize(self): 
		""" Gather some statistics """
		total_vars = self.total_vars_and_nnz[0]
		num_new_constraints = self.sumsq_expr.numConstraints()
		total_constraints = (num_new_constraints + sum([eq_const.numConstraints() for eq_const in self.eq_consts]))

		""" Create constraint matrices including those implicit constraints """
		constraint_mat = self.createConstraintMat(total_constraints,self.total_vars_and_nnz)
		""" Append a -identity matrix for the dual variables """
		constraint_mat = sparse.hstack(
			[constraint_mat,-1*sparse.eye(constraint_mat.shape[0],num_new_constraints)]).tocsc()

		constraint_const = self.createConstMat(total_constraints,self.total_vars_and_nnz)

		""" Form the KKT system and solve it """
		total_constraints = constraint_const.shape[0]
		KKT_mat = mutils.cat([[mutils.gradMat(total_vars,num_new_constraints),constraint_mat.T],
                              [constraint_mat,mutils.zeros(total_constraints,total_constraints)]])
		KKT_const = sparse.vstack([mutils.zeros(total_vars+num_new_constraints,1),constraint_const])
		solution = linalg.spsolve(KKT_mat.tocsc(),KKT_const)
		
		""" Write results back to the correct variables """
		for var in self.included_vars: var.extractValues(solution)
		self.val = solution[total_vars:total_vars+num_new_constraints].T.dot(solution[total_vars:total_vars+num_new_constraints])
	
	def minimizeLSMR(self):
		""" Gather some statistics """
		total_vars = self.total_vars_and_nnz[0]
		num_new_constraints = self.sumsq_expr.numConstraints()
		total_constraints = (num_new_constraints + sum([eq_const.numConstraints() for eq_const in self.eq_consts]))

		""" Create constraint matrices including those implicit constraints """
		constraint_mat = self.createConstraintMat(total_constraints,self.total_vars_and_nnz)
		""" Append a -identity matrix for the dual variables """
		constraint_mat = sparse.hstack(
			[constraint_mat,-1*sparse.eye(constraint_mat.shape[0],num_new_constraints)]).tocsc()

		constraint_const = self.createConstMat(total_constraints,self.total_vars_and_nnz)

		""" Form the KKT system and solve it """
		total_constraints = constraint_const.shape[0]
		KKT_mat = mutils.cat([[mutils.gradMat(total_vars,num_new_constraints),constraint_mat.T],
                              [constraint_mat,mutils.zeros(total_constraints,total_constraints)]])
		KKT_const = sparse.vstack([mutils.zeros(total_vars+num_new_constraints,1),constraint_const])
		KKT_const = np.array(KKT_const.todense())
		KKT_const = np.squeeze(KKT_const)
		solution,exit_condition = linalg.lsmr(KKT_mat.tocsc(),KKT_const)[0:2]
		
		""" Write results back to the correct variables """
		for var in self.included_vars: var.extractValues(solution)
		self.val = solution[total_vars:total_vars+num_new_constraints].T.dot(solution[total_vars:total_vars+num_new_constraints])
	
	""" Solve this system of equations, only looks at equality constraints """
	def solve(self):
		""" Form the system of equations from the constraints """
		total_constraints = sum([eq_const.numConstraints() for eq_const in self.eq_consts])
		constraint_mat = self.createConstraintMat(total_constraints,self.total_vars_and_nnz)
		constraint_const = self.createConstMat(total_constraints,self.total_vars_and_nnz)
		
		""" Call solve """
		solution = linalg.spsolve(constraint_mat.tocsc(),constraint_const)
		
		""" Extract solution """
		for var in self.included_vars: var.extractValues(solution)