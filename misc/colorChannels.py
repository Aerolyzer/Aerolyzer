# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

'''
Purpose: to provide a multipanel look at the color channels in a given image
Inputs: location to JPG file
Ouputs: a grayscale multipanel image of the R,G,B, yellow, magenta and cyan
		color channels of the ori image. The image is stored at the same location.
'''
import getopt
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def main(argv):

	# get input from user
	try:
	    opts, arg = getopt.getopt(argv, "hf:")

	    if len(opts) == 0:
	        print('Please run: python colorChannels.py -h')
	        sys.exit(2)

	    for opt, arg in opts:
	        if '-h' in opt:
	            print('This is a quick script to view the red, green, blue, yellow, magenta \
	                   and cyan channels in an img')
	            print('To run: python colorChannels.py -f imageFileLoc')
	            print('For example: python colorChannels.py -f /tmp/myImg.jpg')
	            print('The image MUST BE JPG format.')
	            print('If needed, use http://image.online-convert.com/convert-to-png to convert to JPG.')
	            sys.exit(2)
	        elif '-f' in opt: 
	            imgFile = arg
	            if not os.path.exists(imgFile):
	                print('!! File not found!!')
	                sys.exit(2)
	        else:
	            print('Please run: python colorChannels.py -h')
	            sys.exit(2)

	except getopt.GetoptError:
	    print('Please run: python colorChannels.py -h')


	img2 = mpimg.imread(imgFile)

	# color channels are RGB
	# if gray color scale is used, the 'whiter the area/ pixel that means is represents that color'
	# in RGB, R+G = yellow; R+B = magenta (violets); G+B = cyan (lightish green); RBG @ same intensity = white;

	red = img2[:,:,0]

	green = img2[:,:,1]

	blue = img2[:,:,2]

	yellow = img2[:,:,0] + img2[:,:,1]

	magenta = img2[:,:,0] + img2[:,:,2]

	cyan = img2[:,:,1] + img2[:,:,2]

	# Multipanel plot
	f, ax = plt.subplots(3,3)
	f.delaxes(ax[0,0]) 
	f.delaxes(ax[0,2])
	ax[0,1].imshow(img2)
	ax[0,1].set_title('original')
	i = ax[1,0].imshow(red, cmap="gray")
	plt.colorbar(i, ax=ax[1,0])
	ax[1,0].set_title('red')
	i = ax[1,1].imshow(green, cmap="gray")
	plt.colorbar(i, ax=ax[1,1])
	ax[1,1].set_title('green')
	i = ax[1,2].imshow(blue, cmap="gray")
	plt.colorbar(i, ax=ax[1,2])
	ax[1,2].set_title('blue')
	i = ax[2,0].imshow(yellow, cmap="gray")
	plt.colorbar(i, ax=ax[2,0])
	ax[2,0].set_title('yellow')
	i = ax[2,1].imshow(magenta, cmap="gray")
	plt.colorbar(i, ax=ax[2,1])
	ax[2,1].set_title('magenta')
	i = ax[2,2].imshow(cyan, cmap="gray")
	plt.colorbar(i, ax=ax[2,2])
	ax[2,2].set_title('cyan')

	# hide x ticks for top plots and y ticks for right plots
	plt.setp([a.get_xticklabels() for a in ax[0, :]], visible=False)
	plt.setp([a.get_xticklabels() for a in ax[1, :]], visible=False)
	plt.setp([a.get_yticklabels() for a in ax[:, 1]], visible=False)
	plt.setp([a.get_yticklabels() for a in ax[:, 2]], visible=False)

	plt.suptitle(imgFile.split('/')[-1])

	plt.savefig('/'.join(imgFile.split('/')[:-1]) + '/' + imgFile.split('/')[-1].split('.')[0] + 'grayMap.jpg')

if __name__ == '__main__':
    main(sys.argv[1:])