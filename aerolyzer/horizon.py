import sys
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt
from retrieve_image_data import RtrvData as Data


def is_sky(a, path):
    # Create a mask
    data = Data(path)
    img = data.get_rgb(path)
    tags = data.get_exif(path, True, True)
    mask = np.zeros(img.shape[:2], np.uint8)
    mask[0:(img.shape[0] / 2), 0:img.shape[1]] = 255
    masked_img = cv2.bitwise_and(img, img, mask = mask)

    # Create histograms with 16 bins in range 0-255
    color = ('b', 'g', 'r')
    b, g, r = cv2.split(img)
    dimy, dimx = img.shape[:2]

    largest = [0, 0]
    it = dimy / 200 #iterations = total number of rows(pixels) / 200
    for i in range(dimy / 4, (dimy / 4) * 3, it):   #only looking at the middle half of the image
        ravg = (sum(r[i]) / float(len(r[i])))
        gavg = (sum(g[i]) / float(len(g[i])))
        bavg = (sum(b[i]) / float(len(b[i])))
        avg = (ravg + gavg + bavg) / 3
        pravg = (sum(r[i - it]) / float(len(r[i - it])))
        pgavg = (sum(g[i - it]) / float(len(g[i - it])))
        pbavg = (sum(b[i - it]) / float(len(b[i - it])))
        pavg = (pravg + pgavg + pbavg) / 3
        diff = pavg - avg
        if diff > largest[0]:   #only getting the largest intensity drop.
            largest = [diff,i-(it/2)]
    if largest[0] >= 11:
        sky = img[0:largest[1],0:dimx]#cropping out landscape
        h1 = sky[0:(sky.shape[0] / 2),0:dimx]#top half of sky
        h2 = sky[(sky.shape[0] / 2):(sky.shape[0]), 0:dimx]#bottom half

        mask = np.zeros(h1.shape[:2], np.uint8)
        mask[0:(h1.shape[0] / 2), 0:h1.shape[1]] = 255

        for i,col in enumerate(color):
            histr = cv2.calcHist([h1], [i], mask, [255], [0, 255])
            plt.plot(histr, color = col)
            plt.xlim([0,255])

        mask = np.zeros(h2.shape[:2], np.uint8)
        mask[0:(h2.shape[0] / 2), 0:h2.shape[1]] = 255

        for i,col in enumerate(color):
            histr = cv2.calcHist([h2], [i], mask, [255], [0, 255])
            plt.plot(histr, color = col)
            plt.xlim([0, 255])
        return True

    else:
        return False
