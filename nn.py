import numpy as np
def sigm(x):
	return 1 / (1 + np.exp(-x))
def network(X,y):	
	#X = np.array([ [0,0,1],[0,1,1],[1,0,1],[1,1,1] ])
	#y = np.array([[0,1,1,0]]).T
	syn0 = 2*np.random.random((6,(X.size/6))) - 1 #synapse 0 (in between input and hidden layer)	
	syn1 = 2*np.random.random((y.size,1)) - 1 #synapse 1 (in between hidden layer and output)
	for j in xrange(80000):
		l1 = sigm(np.dot(X,syn0)) #hidden layer
		l2 = sigm(np.dot(l1,syn1)) #output layer
		l2_delta = (y - l2)*(l2*(1-l2))
		l1_delta = l2_delta.dot(syn1.T) * (l1 * (1-l1))
		syn1 += l1.T.dot(l2_delta)
		syn0 += X.T.dot(l1_delta)
	#print l2
	

	print "testing with 1484949763_7_417.jpg [.3412,.4549,.5490,.0314,.1216,.3608] [1]"
	X = np.array([.3412,.4549,.5490,.0314,.1216,.3608])
	l1dup = sigm(np.dot(X,syn0))
	l2dup = sigm(np.dot(l1dup,syn1))
	print '%f' % (float(l2dup))

	print "testing with 1484949787_52_1631.jpg [.7843,.4118,.3333,.8235,.4274,.3294] [0]"
	X = np.array([.7843,.4118,.3333,.8235,.4274,.3294])
	print X
	print syn0
	print np.dot(X,syn0)
	l1dup = sigm(np.dot(X,syn0))
	l2dup = sigm(np.dot(l1dup,syn1))
	print '%f' % (float(l2dup))

X = np.array([[.2745,.2,.3647,.2392,.2392,.3804],
	      [.0823,.1059,.1294,.0667,.0941,.1176],
	      [.4470,.0,.0078,.2353,.2039,0.],
	      [.0039,.0,.0,.2549,.4902,.7451],
	      [.698,.5412,.6902,.6274,.6902,.8431],
	      [.4706,.6078,.6157,.3804,.5882,.6157],
	      [.6667,.5804,.5765,.4745,.5686,.5569],
	      [.9529,.9529,.9176,.949,.9294,.8941],
	      [.7098,.7098,.7255,.4784,.4470,.5137],
	      [.2745,.2392,.2510,.0,.0823,.2039],
	      [.2902,.2823,.2823,.2431,.2274,.2274],
	      [.698,.4157,.1686,.8941,.6431,.5412],
	      [.2667,.541,.6588,.5216,.6078,.5412]])
print X
y = np.array([[1],[0],[1],[1],[1],[0],[0],[0],[0],[1],[0],[0],[1]])
network(X,y)
