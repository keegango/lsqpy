"""
"""
import numpy as np
from lsqpy.exprs.affine import Affine
from lsqpy.exprs.variable import Variable

def override(name):
	def ufunc(x, y):
		if isinstance(y, Affine): return NotImplemented
		return getattr(np, name)(x, y)
	return ufunc

np.set_numeric_ops(
	** {
		ufunc : override(ufunc) for ufunc in ("equal")
	}
)