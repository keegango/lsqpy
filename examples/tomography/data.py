"""
Loads the data for the tomography example and plots if called directly
"""

from scipy import sparse
import numpy as np

# Load the data with prints to show progress
line_mat_x = np.genfromtxt('tux_sparse_x.txt')
print('done loading x coordiantes')
line_mat_y = np.genfromtxt('tux_sparse_y.txt')
print('done loading y coordiantes')
line_mat_val = np.genfromtxt('tux_sparse_val.txt')
print('done loading matrix values')
line_vals = np.genfromtxt('tux_sparse_lines.txt')
print('done loading line values')

# Form the sparse matrix from the data
img_size = 50 # Image is 50 x 50
num_pixels = img_size*img_size # The number of pixels in the image
shape = (3300,num_pixels)
line_mat = sparse.coo_matrix((line_mat_val,(line_mat_x,line_mat_y)),shape)

"""
# Plot data if python was called on this file directly
import sys
if(sys.argv[0] == 'data.py'):
	import matplotlib.pyplot as plt
	plt.figure(0)
	plt.plot(line_mat_x,line_mat_y,'ro')
	plt.show()
"""