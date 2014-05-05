import numpy as np

# In this control problem, the object starts from the origin

# Some constraints on our motion
# The object should start from the origin, and end at rest
initial_velocity = np.array([[-20,20]]).T
final_position = np.array([[10,0]]).T
					  
T = 100 # The number of timesteps
h = 0.01 # The time between time intervals

mass = 100 # Mass of object
drag = 0.01 # Drag on object