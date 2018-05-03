import os
import numpy as np
import cv2
def sigm(x):
	return 1 / (1 + np.exp(-x))
def network(X,y):	
	syn0 = 2*np.random.random((6,(X.size/6))) - 1 #synapse 0 (in between input and hidden layer)	
	syn1 = 2*np.random.random((y.size,1)) - 1 #synapse 1 (in between hidden layer and output)
	for j in xrange(80000):
		l1 = sigm(np.dot(X,syn0)) #hidden layer
		l2 = sigm(np.dot(l1,syn1)) #output layer
		l2_delta = (y - l2)*(l2*(1-l2))
		l1_delta = l2_delta.dot(syn1.T) * (l1 * (1-l1))
		syn1 += l1.T.dot(l2_delta)
		syn0 += X.T.dot(l1_delta)
        print syn0.tolist()
        print syn1.tolist()
	l1dup = sigm(np.dot(X,syn0))
	l2dup = sigm(np.dot(l1dup,syn1))


def getin(img):
    
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[0:(img.shape[0] / 2), 0:img.shape[1]] = 255
    masked_img = cv2.bitwise_and(img, img, mask = mask)

    # Create histograms with 16 bins in range 0-255
    color = ('b', 'g', 'r')
    b, g, r = cv2.split(img)
    dimy, dimx = img.shape[:2]

    largest = [0, 0]
    it = dimy / 200 #iterations = total number of rows(pixels) / 200
    for i in range(dimy / 6, (dimy / 6) * 5, it):   #only looking at the middle half of the image
        ravg = (sum(r[i]) / float(len(r[i])))
        gavg = (sum(g[i]) / float(len(g[i])))
        bavg = (sum(b[i]) / float(len(b[i])))
        avg = (ravg + gavg + bavg) / 3
        pravg = (sum(r[i - it]) / float(len(r[i - it])))
        pgavg = (sum(g[i - it]) / float(len(g[i - it])))
        pbavg = (sum(b[i - it]) / float(len(b[i - it])))
        pavg = (pravg + pgavg + pbavg) / 3
        diff = pavg - avg
        if diff > largest[0]:   #only getting the largest intensity drop.
            largest = [diff,i-(it/2)]
    sky = img[0:largest[1], 0:dimx]#cropping out landscape
    h1 = sky[0:(sky.shape[0] / 2), 0:dimx]#top half of sky
    h2 = sky[(sky.shape[0] / 2):(sky.shape[0]), 0:dimx]#bottom half
    mask1 = np.zeros(h1.shape[:2], np.uint8)
    mask1[0:(h1.shape[0] / 2), 0:h1.shape[1]] = 255
    hist1 = [0,0,0]
    hist2 = [0,0,0]
    max1 = [0,0,0]
    max2 = [0,0,0]
    for i,col in enumerate(color):
        hist1[i] = cv2.calcHist([h1], [i], mask1, [255], [0, 255])
        max1[i] = np.argmax(hist1[i][6:250])

    mask2 = np.zeros(h2.shape[:2], np.uint8)
    mask2[0:(h2.shape[0] / 2), 0:h2.shape[1]] = 255
    for j,col in enumerate(color):
        hist2[j] = cv2.calcHist([h2], [j], mask2, [255], [0, 255])
        max2[j] = np.argmax(hist2[j][6:250])
    x = [float(max1[0])/255., float(max1[1])/255., float(max1[2])/255., float(max2[0])/255., float(max2[1])/255., float(max2[2])/255.]
    return x


x = []
y = []

for file in os.listdir("./good-imgs"):
    pathname = "./good-imgs/" + file
    img = cv2.imread(pathname,1)
    x.append(getin(img))
    y.append([1])
for file in os.listdir("./bad-imgs"):
    pathname = "./bad-imgs/" + file
    img = cv2.imread(pathname,1)
    x.append(getin(img))
    y.append([0])
x = np.array(x)
y = np.array(y)

network(x,y)



