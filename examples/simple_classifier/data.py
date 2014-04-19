import numpy as np

np.random.seed(0)

n = 200

true_vect = np.array([[-0.7071,0.7071]]).T

X = np.random.standard_normal(size=(n,2))*2
y = np.sign(X.dot(true_vect)+np.random.standard_normal(size=(n,1)))

# Set to True if you want to plot the data
if(False):
	import matplotlib.pyplot as plt
	plt.plot(X[y[:,0]>=0,0],X[y[:,0]>=0,1],'ro')
	plt.plot(X[y[:,0]<0,0],X[y[:,0]<0,1],'bo')
	plt.xlabel('x')
	plt.ylabel('y')
	plt.show()