'''
Image Restriction Function File
Description: This file contains all functions for the verifying image restrictions.
'''
import os
import re
import cv2
import yaml
from datetime import datetime
import exifread
import numpy as np

class imgRestFuncs(object):
    'Class containing all image restriction functions'
    '''
    Purpose:        sigmoid function that takes in a value and returns a value from 0 to 1
    Inputs:         float
    Outputs:        None
    Returns:        Float between 0, 1
    Assumptions:    N/A
    '''
    def sigm(self, x):
        return 1 / (1 + np.exp(-x))

    def __init__(self):
        self.criteria = self._import_yaml(os.getcwd() + "/../../Aerolyzer/aerolyzer/config/image_restriction_conf.yaml")

    '''
    Purpose:        The purpose of this function is to determine whether or not the device the
                    image was taken on is an accepted mobile device.
    Inputs:         string device
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_device(self, device):
        if device in self.criteria['acceptedMobileDevices']:
            return True
        else:
            return False


    '''
    Purpose:        The purpose of this function is to determine whether or not the image was
                    altered from its original form. I.e. do the modification and creation dates coincide.
    Inputs:         datetime created, datetime modified
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_edited(self, modified, created):
        if (created == modified):
            return True
        else:
            return False

    '''
    Purpose:        The purpose of this function is to determine whether or not the image
                    contains a direct landscape with sky and view.
    Inputs:         tuple lists of lists of rgb values (red, green, blue)
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_landscape(self, img):
        # Create a mask
        #mask = np.zeros(img.shape[:2], np.uint8)
        #mask[0:(img.shape[0]/2), 0:img.shape[1]] = 255
        #masked_img = cv2.bitwise_and(img,img,mask = mask)

        # Create histograms with 16 bins in range 0-255
        #hist_blue = cv2.calcHist([img],[0],mask,[16],[0,255])
        #hist_green = cv2.calcHist([img],[1],mask,[16],[0,255])
        #hist_red = cv2.calcHist([img],[2],mask,[16],[0,255])
        return self._is_sky(img)

    '''
    Purpose:        The purpose of this function is to determine whether or not the size of
                    the image is less than or equal to 200kb.
    Inputs:         dict exifData, int imgMaxSize, int imgMaxSizeBytesShort,
                    string fileSize
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_size(self, fileSize):
        if(fileSize > self.criteria['imgMaxSizeNumber']):
            return False
        else:
            return True

    '''
    Purpose:        The purpose of this function  is to determine whether or not the image is
                    an accepted file type.
    Inputs:         string fileType
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_type(self, fileType):
        if fileType in self.criteria['acceptedFileTypes']:
            return True
        else:
            return False

    '''
    Purpose:        The purpose of this function is to determine whether or not the image
                    exceeds the minimum resolution.
    Inputs:         int imageWidth, int imageLength
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_res(self, imageWidth, imageLength):
        if (imageWidth >= self.criteria['imgWidthMin']) and (imageLength >= self.criteria['imgLengthMin']):
            if (imageWidth <= self.criteria['imgWidthMax']) and (imageLength <= self.criteria['imgLengthMax']):
                return True
        else:
            return False

    '''
    Purpose:        The purpose of this function is to determine whether or not the image contains
                    a valid sky or not. 
    Inputs:         image
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def _is_sky(self, img):
        syn0 = np.array([
                        [0.75627016, -0.24375051, -1.01208743, -2.82196649, -2.13659437, 1.44774139, -3.42969981, -2.30166462, 0.16540564, -5.46942492, -0.89061896, -3.05775917, 13.78175927],
                        [4.01459384, 6.80890819, -1.33467051, -8.6509415, -0.97254904, 7.65391215,  2.80460369, -7.96453625, -0.78258749,  0.23794325, -3.05427998, -1.08719948, -1.05505044],
                        [-2.99415349, -5.03765458,  0.95907762, 6.2100258, -0.77418415, -6.45073556, -4.28959853,  6.4269825, 0.08357833, -1.34192387, 2.45324273, -1.88004736, -2.17461887],
                        [-1.33260449, -0.06806694, -0.54152864, 2.29643921, -1.49527328, -0.27464986,  1.61048268,  1.87987677, -0.71722108, -0.31390847, 1.09973296, -0.71580621, -11.78420703],
                        [0.41402219, 0.13775545,  0.17955999, 1.53319054, -0.37451253, -0.19688275, -1.56439065, -0.60001667, -1.31350033, -0.1028686, 0.2385619, -0.98948445, -7.51238318],
                        [-1.28689963, -1.83018296,  0.95150202, 0.35453703, -1.4224101, -1.45727839, -2.11189616,  1.74252963, -1.71482389, -2.29710027, 0.59118241, -0.89214872, -3.12445739]])
        syn1 = np.array([
                        [ -5.93204166],
                        [ -8.12550549],
                        [  0.18872795],
                        [  8.65136128],
                        [ -3.49798356],
                        [ -9.83118546],
                        [ -8.08570886],
                        [  8.19601228],
                        [ -1.44990589],
                        [ -9.531507  ],
                        [  2.54965604],
                        [ -5.09832493],
                        [ 18.47629354]])
        mask = np.zeros(img.shape[:2], np.uint8)
        mask[0:(img.shape[0] / 2), 0:img.shape[1]] = 255
        masked_img = cv2.bitwise_and(img, img, mask = mask)

        # Create histograms with 16 bins in range 0-255
        color = ('b', 'g', 'r')
        b, g, r = cv2.split(img)
        dimy, dimx = img.shape[:2]

        largest = [0, 0]
        it = dimy / 200 #iterations = total number of rows(pixels) / 200
        for i in range(dimy / 6, (dimy / 6) * 5, it):   #only looking at the middle half of the image
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
        sky = img[0:largest[1], 0:dimx]#cropping out landscape
        h1 = sky[0:(sky.shape[0] / 2), 0:dimx]#top half of sky
        h2 = sky[(sky.shape[0] / 2):(sky.shape[0]), 0:dimx]#bottom half
        mask1 = np.zeros(h1.shape[:2], np.uint8)
        mask1[0:(h1.shape[0] / 2), 0:h1.shape[1]] = 255
        hist1 = [0,0,0]
        hist2 = [0,0,0]
        max1 = [0,0,0]
        max2 = [0,0,0]
        for i,col in enumerate(color):
            hist1[i] = cv2.calcHist([h1], [i], mask1, [255], [0, 255])
            max1[i] = np.argmax(hist1[i][6:250])
    
        mask2 = np.zeros(h2.shape[:2], np.uint8)
        mask2[0:(h2.shape[0] / 2), 0:h2.shape[1]] = 255
        for j,col in enumerate(color):
            hist2[j] = cv2.calcHist([h2], [j], mask2, [255], [0, 255])
            max2[j] = np.argmax(hist2[j][6:250])
        X = np.array([float(max1[0])/255., float(max1[1])/255., float(max1[2])/255., float(max2[0])/255., float(max2[1])/255., float(max2[2])/255.])
        l1dup = self.sigm(np.dot(X,syn0))
        l2dup = self.sigm(np.dot(l1dup,syn1))
        if float(l2dup) >= 0.5:
            return True
        return False 


    '''
    Purpose:        The purpose of this function is to import the contents of the configuration file.
    Inputs:         string conf_file
    Outputs:        None
    Returns:        reference to configuration file
    Assumptions:    N/A
    '''
    def _import_yaml(self, confFile):
        with open(confFile, 'r') as f:
            doc = yaml.load(f)
            f.close()
        return doc
