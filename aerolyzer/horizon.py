import sys
import cv2
import numpy as np

class horizon:
	
	def __init__(self):
		self.message = "Hello World"
	

	def _hello(self,i):
		x=0
		while x<i:
			print self.message
			x = x + 1
		return 0


	def getHorizon(self, directory):
		for image in directory: 
		img_noblur = cv2.imread("/home/aero/Desktop/Aerolyzer/images/A/1.jpg")
		img = cv2.blur(img_noblur, (7,7))

		edges = cv2.Canny(img,55,110) #magic numbers (min & max tolerance)

		lines = cv2.HoughLines(edges,1,np.pi/180,10) #magic numbers (min line length)
		for rho,theta in lines[0]:
		    a = np.cos(theta)
		    b = np.sin(theta)
		    x0 = a*rho
		    y0 = b*rho
		    x1 = int(x0 + 1000*(-b))
		    y1 = int(y0 + 1000*(a))
		    x2 = int(x0 - 1000*(-b))
		    y2 = int(y0 - 1000*(a))
		    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

		cv2.imwrite('houghlines3.jpg',img)
			
