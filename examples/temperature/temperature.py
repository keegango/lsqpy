"""
Analyze global temperature data by detrending a yearly component
"""

from lsqpy import Variable, sum_squares, minimize
from data import temperatures, num_samples
import matplotlib.pyplot as plt
import numpy as np

yearly_tread = Variable(num_samples)
a = Variable()
b = Variable()

equality_constraints = []
for i in range(12,num_samples):
	equality_constraints.append(yearly_tread[i] == yearly_tread[i-12])
	
t = np.array([list(range(0,num_samples))]).T
t2 = np.power(t,2)

smoothing = 0.0001
objective = sum_squares(yearly_tread + t*b + t2*a - temperatures)
objective += smoothing*sum_squares(yearly_tread[0:num_samples-1] - yearly_tread[1:num_samples])

minimize(objective,equality_constraints)

plt.figure(0)
plt.plot(temperatures)
plt.plot(yearly_tread.value + t*b.value + t2*a.value,'r')
plt.show()

plt.figure(1)
plt.plot(yearly_tread.value + t*b.value + t2*a.value - temperatures)
plt.show()