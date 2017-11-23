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


		#The following equalizes the histogram of an image
		img_YUV = cv2.cvtColor(imgOg,cv2.COLOR_BGR2YCR_CB) # Convert to ycrb
		b, r, g = cv2.split(img_YUV) # Split into blue-green-red channels
		cv2.equalizeHist(b) # Equalize Blue Channel
		cv2.equalizeHist(g) # Equalize Blue Channel
		imgBlueEqu = cv2.merge((b, r, g)) # Merge blue back into RGB
		img_BGR = cv2.cvtColor(imgOg,cv2.COLOR_YCR_CB2BGR) # Convert to BGR

		blur = cv2.GaussianBlur(img_BGR,(5,5),0) # Perform a gaussian blur

		img_GREY = cv2.cvtColor(blur,cv2.COLOR_BGR2GRAY) # Convert to Greyscale

		ret, thresh = cv2.threshold(img_GREY,127,255,cv2.THRESH_BINARY) # Threshold image to segment sky

		# Perform erosian and dialiation to isolate the sky
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5), (3,3))
		img_erode = cv2.erode(thresh, kernel)
		img_dilate = cv2.dilate(img_erode, kernel)

		img, contours, hierarchy = cv2.findContours(img_dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
		
		final = cv2.drawContours(imgOg, contours, -1, (0,255,0), 3)

		cv2.imwrite(output+"H_"+image,final) # Write to file