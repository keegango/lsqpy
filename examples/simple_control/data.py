import numpy as np

# In this control project, the object must reach these points
# at the 1/4, 1/2, and 3/4 time marks. It should start from the
# origin with zero velocity, and end at the origin also with zero
# velocity.

# Some way points
waypoints = np.array([[0,-2,6,-2,-4,4,0],
                      [0, 8,6,-5, 5,3,0]])

import sys
if(sys.argv[0] == 'data.py'):
	import matplotlib.pyplot as plt
	plt.figure(0)
	plt.plot(waypoints[0,:],waypoints[1,:],'bo')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.show()