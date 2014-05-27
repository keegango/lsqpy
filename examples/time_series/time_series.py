from lsqpy import Variable, sum_squares, minimize
import matplotlib.pyplot as plt
import numpy as np

# Import data for the problem
from data import temps, n

seasonal = Variable(n)

eq_constraints = []
for i in range(365,n): eq_constraints.append(seasonal[i] == seasonal[i-365])

smoothing = 0
smooth_objective = sum_squares(seasonal[0:n-1] - seasonal[1:n])
minimize(sum_squares(temps - seasonal) + smoothing*smooth_objective,eq_constraints)

residuals = temps - seasonal.value

# Generate the residuals matrix
matlist = []
ar_len = 5
for i in range(ar_len): matlist.append(residuals[ar_len-i-1:n-i-1])
residuals_mat = np.hstack(matlist)

# Solve autoregressive problem
ar_coef = Variable(ar_len)
minimize(sum_squares(residuals_mat*ar_coef - residuals[ar_len:]))
print(ar_coef.value)

# Do all plotting
plt.figure(0)
plt.plot(temps)
plt.plot(seasonal.value,'r')
plt.title('seasonal fit against data')

plt.figure(1)
plt.plot(residuals[ar_len:],'g')
plt.plot(residuals_mat.dot(ar_coef.value),'r')
plt.title('autoregressive fit against residuals')

plt.figure(2)
plt.plot(temps)
total_estimate = seasonal.value
total_estimate[ar_len:] += residuals_mat.dot(ar_coef.value)
plt.plot(total_estimate,'r')
plt.title('total fit vs data')

plt.show()