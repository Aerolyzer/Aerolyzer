<<<<<<< HEAD
import os
from aerolyzer import horizon
def all_images(directory, output):
	included_extensions = ['jpg']
	files = [fn for fn in os.listdir(directory) if any(fn.endswith(ext) for ext in included_extensions)]
	for image in files:
		horizon().getHorizon(str(directory), image, output)

=======
import aerolyzer

aerolyzer.test()
>>>>>>> upstream/master



directory = "../test_images/"
output = "/media/sf_transfer/results/"
all_images(directory, output)

#horizon().getHorizon(directory, "92.jpg", output)