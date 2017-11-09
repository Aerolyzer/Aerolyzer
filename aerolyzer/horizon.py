import sys
import cv2
import os
import numpy as np

class horizon:
	
	def _testAnalyze(self, directory):
		included_extensions = ['jpg']
		files = [fn for fn in os.listdir(directory) if any(fn.endswith(ext) for ext in included_extensions)]
		for image in files:
			self.getHorizon(str(directory), image)

	def getHorizon(self, directory, image):
		img_noblur = cv2.imread(str(directory)+image)
		img = cv2.blur(img_noblur, (7,7))
		edges = cv2.Canny(img,55,110) #magic numbers (min & max tolerance)
		lines = cv2.HoughLines(edges,1,np.pi/180,10) #magic numbers (min line length)
		print(str(lines))
		for rho,theta in lines[0]:
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
			
