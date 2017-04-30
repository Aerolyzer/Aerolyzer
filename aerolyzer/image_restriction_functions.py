'''
Image Restriction Function File
Description: This file contains all functions for the verifying image restrictions.
'''

import re
import cv2
import yaml
from datetime import datetime
import exifread
import numpy as np

class imgRestFuncs(object):
    'Class containing all image restriction functions'

    def __init__(self):
        self.criteria = self._import_yaml("config/image_restriction_conf.yaml")

    '''
    Purpose:        The purpose of this function is to determine whether or not the device the
                    image was taken on is an accepted mobile device.
    Inputs:         string device
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_device(self, device):
        assert (type(device) == str), "Device value not a string"
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
    def is_edited(self, created, modified):
        assert (type(created) == datetime), "Image DateTime value not a datetime"
        assert (type(modified) == datetime), "EXIF DateTimeOriginal value not a datetime"
        
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
        mask = np.zeros(img.shape[:2], np.uint8)
        mask[0:(img.shape[0]/2), 0:img.shape[1]] = 255
        masked_img = cv2.bitwise_and(img,img,mask = mask)

        # Create histograms with 16 bins in range 0-255
        hist_blue = cv2.calcHist([img],[0],mask,[16],[0,255])
        hist_green = cv2.calcHist([img],[1],mask,[16],[0,255])
        hist_red = cv2.calcHist([img],[2],mask,[16],[0,255])

        return self._is_sky(hist_blue, hist_green, hist_red)

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
        assert (type(fileType) == str), "File Type value not a string"

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
        assert (type(imageWidth) == int), "EXIF ExifImageWidth value not an integer"
        assert (type(imageLength) == int), "EXIF ExifImageLength value not an integer"

        if (imageWidth >= self.criteria['imgWidthMin']) and (imageLength >= self.criteria['imgLengthMin']):
            if (imageWidth <= self.criteria['imgWidthMax']) and (imageLength <= self.criteria['imgLengthMax']):
                return True
        else:
            return False

    '''
    Purpose:        The purpose of this function is to determine whether or not the image was
                    taken by a device with location services enabled for the camera.
    Inputs:         string gpsLat, string gpsLon
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_loc(self, gpsLat, gpsLon):
        if (gpsLat != '' and gpsLon != ''):
            return True
        else:
            return False

    '''
    Purpose:        The purpose of this function is to determine whether or not the I and
                    II quadrants of the image have rgb values indicitive of a sky
    Inputs:         list of lists red_sky, list of lists green_sky, list of lists blue_sky
                    Note: Each inner list contains rgb for each pixel in a horizontal row
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def _is_sky(self, red, green, blue):
        maxIndexRed = np.argmin(red)
        maxIndexBlue = np.argmin(blue)
        maxIndexGreen = np.argmin(green)

        #insert code to determine if range of max values is accepted as a sky

        return True 

    '''
    Purpose:        The purpose of this function is to import the contents of the configuration file.
    Inputs:         string conf_file
    Outputs:        None
    Returns:        reference to configuration file
    Assumptions:    N/A
    '''
    def _import_yaml(self, confFile):
        assert (type(confFile) == str), "configuration file not passed as a string"        
        with open(confFile, 'r') as file:
            doc = yaml.load(file)
            file.close()
        return doc
