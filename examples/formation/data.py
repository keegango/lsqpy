"""
Data for formation flying
Ships should start from the origin
"""

from lsqpy import Variable, sum_squares, minimize
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

n = 5

T = 500 # The number of timesteps
h = 0.01 # The time between time intervals

mass = 100 # Mass of object
drag = 0.01 # Drag on object

speeds0 = 10*np.array([[1, -1, -1, 1, 1],[0, 0,1,1,0]])

formation1_start = 100
formation1_end = 200
# Formation is specified by position with respect to first ship
formation1 = 0.5*np.array([[-1, -1, 1, 1],[-1, 1, -1, 1]])

formation2 = 0.5*np.array([[-2, -1, 1, 2],[0, 0, 0, 0]])

# Declare variables representing the location and movement of the ships
positions = [Variable(2,T) for _ in range(n)]
velocities = [Variable(2,T) for _ in range(n)]
forces = [Variable(2,T-1) for _ in range(n)]

constraints = []
# Add dynamics constraints
for ship in range(n):
	for i in range(T-1):
		constraints.append(positions[ship][:,i+1] == positions[ship][:,i] + h * velocities[ship][:,i])
	for i in range(T-1):
		constraints.append(velocities[ship][:,i+1] == velocities[ship][:,i] + h/mass * forces[ship][:,i] - drag*velocities[ship][:,i])
	constraints.append(positions[ship][:,0] == 0)
	constraints.append(velocities[ship][:,0] == speeds0[:,ship:ship+1])
	constraints.append(positions[ship][:,300] == speeds0[:,ship:ship+1])
	if ship == 0:
		constraints.append(positions[ship][:,formation1_end] == np.array([[20,-20]]).T)
		constraints.append(positions[ship][:,400] == np.array([[-20,20]]).T)
		constraints.append(positions[ship][:,499] == np.array([[10,-20]]).T)
	else:
		for t in range(formation1_start,formation1_end):
			constraints.append(positions[ship][:,t] - positions[0][:,t] == formation1[:,ship-1:ship])
		for t in range(400,500):
			constraints.append(positions[ship][:,t] - positions[0][:,t] == formation2[:,ship-1:ship])

objective = sum_squares(forces[0])
for i in range(1,n): objective += sum_squares(forces[i])
minimize(objective,constraints)

# Plot paths
fig = plt.figure(0)
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-25, 25), ylim=(-25, 25))

line, = ax.plot([], [], 'o-', lw=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

def init():
	line.set_data([], [])
	time_text.set_text('')
	return line, time_text
	
def animate(i):
	thisx = [positions[ship].value[0,i] for ship in range(n)]
	thisy = [positions[ship].value[1,i] for ship in range(n)]
	line.set_data(thisx, thisy)
	time_text.set_text(time_template%(i*h))
	return line, time_text

ani = animation.FuncAnimation(fig, animate, np.arange(1, T), interval=25, blit=True, init_func=init)
plt.show()