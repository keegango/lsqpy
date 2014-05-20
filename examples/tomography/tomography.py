"""
An example of tomography
"""

from lsqpy import Variable, sum_squares, minimize

from data import img_size, num_pixels, line_mat, line_vals

x = Variable(num_pixels)

objective = sum_squares(x.__rmul__(line_mat) - line_vals)

"""
import cProfile, pstats, io
pr = cProfile.Profile()
pr.enable()	
"""

minimize(objective,solver_type='iterative')

"""
pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
"""
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.figure(0)
plt.imshow(x.value.reshape(img_size,img_size).T,cmap = cm.Greys_r)
plt.show()