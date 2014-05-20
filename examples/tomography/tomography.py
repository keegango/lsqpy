"""
An example of tomography
"""

from lsqpy import Variable, sum_squares, minimize

from data import img_size, num_pixels, line_mat, line_vals

x = Variable(num_pixels)

minimize(line_mat*x - line_vals)

import matplotlib.pyplot as plt
plt.figure(0)
plt.imshow(x.value.reshape(img_size,img_size))
plt.show()