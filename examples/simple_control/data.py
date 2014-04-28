import numpy as np

# In this control problem, the object starts from the origin and should
# reach these waypoints at evenly spaced intervals over its trip

# Some way points
waypoints = np.array([[0,-2,6,-2,-4,4,0],
                      [0, 8,6,-5, 5,3,0]])
					  
T = 100 # The number of timesteps
h = 0.01 # The time between time intervals

mass = 100 # Mass of object
drag = 0.1 # Drag on object

import sys
if(sys.argv[0] == 'data.py'):
	import matplotlib.pyplot as plt
	plt.figure(0)
	plt.plot(waypoints[0,:],waypoints[1,:],'bo')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.show()