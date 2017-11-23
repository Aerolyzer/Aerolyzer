import os
import aerolyzer
def all_images(directory, output):
	included_extensions = ['jpg']
	files = [fn for fn in os.listdir(directory) if any(fn.endswith(ext) for ext in included_extensions)]
	for image in files:
		#aerolyzer.Horizon(directory, image, output)
		aerolyzer.Horizon(directory, image)



directory = "../test_images/"
#output ="/media/sf_transfer/results/"
output = ""
all_images(directory, output)

#aerolyzer.Horizon(directory, "92.jpg")