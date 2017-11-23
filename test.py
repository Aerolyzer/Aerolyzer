import os
import aerolyzer
def all_images(directory, output):
	included_extensions = ['jpg']
	files = [fn for fn in os.listdir(directory) if any(fn.endswith(ext) for ext in included_extensions)]
	for image in files:
		#aerolyzer.getHorizon(directory, image, output)
		aerolyzer.getHorizon(directory, image)



directory = "../test_images/"
#output ="/media/sf_transfer/results/"
output = ""
all_images(directory, output)

#aerolyzer.getHorizon(directory, "92.jpg", output)