import sys
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

class horizon:
	
	def _testAnalyze(self, directory, output):
		included_extensions = ['jpg']
		files = [fn for fn in os.listdir(directory) if any(fn.endswith(ext) for ext in included_extensions)]
		for image in files:
			self.getHorizon(str(directory), image, output)

	def getHorizon(self, directory, image, output):
		img_original = cv2.imread(str(directory)+image) # Read image
		grey = cv2.cvtColor(img_original,cv2.COLOR_BGR2GRAY)
		ret,thresh = cv2.threshold(grey,127,255,0)
		img, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
		cv2.imwrite(output+"H_"+image,img)
