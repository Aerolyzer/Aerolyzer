import sys
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

def test():
	print "hi"
def _testAnalyze(self, directory):
	included_extensions = ['jpg','JPG']
	files = [fn for fn in os.listdir(directory) if any(fn.endswith(ext) for ext in included_extensions)]
	for image in files:
		img_noblur = cv2.imread(str(directory)+image)
		img_noblur = cv2.cvtColor(img_noblur, cv2.COLOR_BGR2GRAY)
		self.getHorizon(str(directory), img_noblur,image)

def getHorizon(self, directory, img_noblur,image):
	img = cv2.blur(img_noblur, (10,10))
	img = cv2.equalizeHist(img)
	img = cv2.equalizeHist(img)
	img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	edges = cv2.Canny(img,150,200) #magic numbers (min & max tolerance)
	plt.subplot(121),plt.imshow(img,cmap = 'gray')
	plt.title('Original Image'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(edges,cmap = 'gray')
	plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
	plt.show()
	lines = cv2.HoughLines(edges,1,np.pi/180,10) #magic numbers (min line length)
	print(str(lines))
	for rho,theta in lines[0]:
	    if (theta > 5.49  or theta < 0.78) or (theta > 2.35 and theta < 3.92): #limiting angle so that it is not more than 45 deg or less than -45
		continue
	    a = np.cos(theta)
	    b = np.sin(theta)
	    x0 = a*rho
	    y0 = b*rho
	    x1 = int(x0 + 1000*(-b))
	    y1 = int(y0 + 1000*(a))
	    x2 = int(x0 - 1000*(-b))
	    y2 = int(y0 - 1000*(a))
	    cv2.line(img_noblur,(x1,y1),(x2,y2),(0,255,0),2)
	cv2.imwrite("results/H_"+image,img_noblur)

#horizon()._testAnalyze("./images/")
			
