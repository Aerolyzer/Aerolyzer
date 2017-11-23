import cv2
import os
import sys
import numpy as np

class horizon:
	
	def _testAnalyze(self, directory, output):
		included_extensions = ['jpg']
		files = [fn for fn in os.listdir(directory) if any(fn.endswith(ext) for ext in included_extensions)]
		for image in files:
			self.getHorizon(str(directory), image, output)

	def getHorizon(self, directory, image, output):
		imgOg = cv2.imread(str(directory)+image) # Read image

		img_YUV = cv2.cvtColor(imgOg,cv2.COLOR_BGR2YCR_CB) # Convert to ycrb

		b, r, g = cv2.split(img_YUV) # Split into blue-green-red channels
		equ = cv2.equalizeHist(b) # Equalize Blue Channel
		imgBlueEqu = cv2.merge((b, r, g)) # Merge blue back into RGB

		img_BGR = cv2.cvtColor(imgOg,cv2.COLOR_YCR_CB2BGR) # Convert to BGR

		cv2.imwrite(output+"H_"+image,img_BGR) # Write to file

		#ret,thresh = cv2.threshold(grey,127,255,0)

		#img, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

		#img = cv2.drawContours(img, contours, -1, (0,255,0), 3)


		#cv2.imwrite(output+"H_"+image,img) # Write to file
