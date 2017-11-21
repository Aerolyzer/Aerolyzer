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
		cv2.imwrite("/media/sf_transfer/results/H_"+image,img_noblur)
			

	def test_algo(self, directory, image):
		intrinsic = np.array(
		[[ 299.39646639,    0.,          419.96165812],
		 [   0.,          302.5602385,   230.25411049],
		 [   0.,            0.,            1.        ]]
		)

		distortion = np.array(
		[-0.16792771, 0.03121603, 0.00218195, -0.00026904, -0.00263317]
		)

		img = cv2.imread(directory+image)
		height, width, channels = img.shape

		img = cv2.undistort(img, intrinsic, distortion)
		edges = cv2.Canny(
			cv2.resize(cv2.split(img)[0], (width / 4, height / 4), 0, 0, cv2.INTER_NEAREST),
			200, 600, apertureSize=3)
		vx, vy, x0, y0 = cv2.fitLine(np.argwhere(edges == 255), 2, 0, 0.01, 0.01)  # 2 = CV_DIST_L2
		print("%.6f,%.6f,%.6f,%.6f\n" % (vx * 4, vy * 4, x0 * 4, y0 * 4))
		cv2.line(img,(vx,vy),(x0,y0),(0,255,0),2)

		cv2.imwrite("/media/sf_transfer/results/H_"+image,img_noblur)