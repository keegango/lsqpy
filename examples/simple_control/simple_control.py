# Import lsqpy
from lsqpy import Variable,sum_sq,minimize

# Import numpy and plotting
import numpy as np
import matplotlib.pyplot as plt

# Import the way points
from data import waypoints,T,h,mass,drag

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
	
# Add waypoint constraints
zero_vector = np.array([[0,0]]).T
for i in range(6): constraints.append(position[:,T*i//6] == waypoints[:,i:i+1])
constraints.append(position[:,T-1] == zero_vector)

# Add velocity constraints
constraints.append(velocity[:,0] == zero_vector)
constraints.append(velocity[:,T-1] == zero_vector)

# Solve the problem
mu = 1#*10**7
minimize(mu*sum_sq(velocity)+sum_sq(force),constraints)

# Plot the points
plt.figure(0)
plt.quiver(position.value[0,0:T-1],position.value[1,0:T-1],
	force.value[0,:].squeeze(),force.value[1,:])
plt.quiver(position.value[0,:],position.value[1,:],
	velocity.value[0,:],velocity.value[1,:],color='g',headaxislength=5)
plt.plot(position.value[0,:],position.value[1,:],'r')
plt.plot(waypoints[0,:],waypoints[1,:],'bo')
plt.xlim([-6,7])
plt.show()