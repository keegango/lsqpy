# Import lsqpy
from lsqpy import Variable, sum_squares, minimize

# Import plotting
import matplotlib.pyplot as plt

# Import the way points
from data import initial_velocity, final_position, T, h, mass, drag

# Declare the variables we need
position = Variable(2,T)
velocity = Variable(2,T)
force = Variable(2,T-1)

# Create the list of constraints on our variables
constraints = []
for i in range(T-1):
	constraints.append(position[:,i+1] == position[:,i] + h * velocity[:,i])
for i in range(T-1):
	constraints.append(velocity[:,i+1] == velocity[:,i] + h/mass * force[:,i] - drag*velocity[:,i])
	
# Add position constraints
constraints.append(position[:,0] == 0)
constraints.append(position[:,T-1] == final_position)

# Add velocity constraints
constraints.append(velocity[:,0] == initial_velocity)
constraints.append(velocity[:,T-1] == 0)

# Solve the problem
mu = 1
minimize(mu*sum_squares(velocity)+sum_squares(force),constraints)

# Plot the points
plt.figure(0,(4,4))
plt.quiver(position.value[0,0:T-1:2],position.value[1,0:T-1:2],
	force.value[0,::2],force.value[1,::2])
plt.plot(position.value[0,:],position.value[1,:],'r')
plt.plot(0,0,'bo')
plt.plot(final_position[0],final_position[1],'bo')
plt.xlim([-2,12]), plt.ylim([-1,4])
plt.show()