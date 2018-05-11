'''
Data Retrieval File
Description: This file contains all functions for retrieving data from an image.
'''

import os
import cv2
import yaml
import exifread
import numpy as np
from datetime import datetime

class RtrvData(object):
    'Class containing all image restriction functions'

    def __init__(self, pathPassed):
        retrieve_conf = {'selectTags': ['Image Model', 'Image DateTime', 'EXIF DateTimeOriginal', 'EXIF ExifImageWidth', 'EXIF ExifImageLength', 'GPS GPSLatitude', 'GPS GPSLongitude', 'GPS GPSLatitudeRef', 'GPS GPSLongitudeRef'], 'intTags': ['exif exifimagewidth', 'exif exifimagelength'], 'datetimeTags': ['image datetime', 'exif datetimeoriginal'], 'stringTags': ['image model', 'gps gpslatitude', 'gps gpslongitude', 'gps gpslatituderef', 'gps gpslongituderef']}
        if os.path.exists(pathPassed + "/config/retrieve_image_data_conf.yaml"):
            self.data = self._import_yaml(pathPassed + "/config/retrieve_image_data_conf.yaml")
        else:
            if not os.path.exists(pathPassed + "/config/"):
                os.makedirs(os.getcwd() + pathPassed + "/config/")
            with open(pathPassed + "/config/retrieve_image_data_conf.yaml", 'w') as outfile:
                yaml.dump(retrieve_conf, outfile, default_flow_style=False)
        self.data = self._import_yaml(pathPassed + "/config/retrieve_image_data_conf.yaml")
        try:
            os.path.exists(pathPassed)
        except ImportError:
            pass


    def _get_all_exif(self, pathname):
        '''
        Purpose:        The purpose of this function is to retrieve the EXIF data from an
                        image.
        Inputs:         string pathname
        Outputs:        None
        Returns:        dictionary of EXIF data tags
        Assumptions:    The image's path has been provided
        '''
        img = open(pathname, 'rb')
        tags = exifread.process_file(img)
        return tags


    def get_exif(self, pathname, setTypes, dateToString):
        '''
        Purpose:        The purpose of this function is to retrieve the EXIF data from an
                        image.
        Inputs:         string pathname
                        bool setTypes toggles conversion of types
                        bool dateToString toggles conversion of dateToString
        Outputs:        None
        Returns:        dictionary of EXIF data tags
        Assumptions:    The image's path has been provided
        '''
        tags = {};
        allTags = self._get_all_exif(pathname)
        for key, value in allTags.iteritems():
            for entry in self.data["selectTags"]:
                if (key == entry):
                    tags[key.lower()] = value
        if setTypes is True:
            tags = self._set_types(tags, dateToString)
        tags['file size'] = self._get_file_size(pathname)
        tags['file type'] = self._get_file_type(pathname).lower()
        return tags


    def get_hsv(self, pathname):
        '''
        Purpose:        The purpose of this function is to retrieve the HSV values from an
                        image's haze layer.
        Inputs:         string pathname
        Outputs:        None
        Returns:        list of lists containing HSV values
        Assumptions:    The image's path has been provided
        '''
        img = cv2.imread(pathname,1)
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
        h2 = sky[(sky.shape[0] / 4)*3:(sky.shape[0]), 0:dimx]#bottom half
        hsv = cv2.cvtColor(h2, cv2.COLOR_BGR2HSV)
        clrlst = []
        dimy, dimx = h2.shape[:2]
        for t in range(1000): #getting 1000 random pixels
            temp = []
            x = int(np.random.random()*10000) % dimx
            y = int(np.random.random()*10000) % dimy
            for k in xrange(len(hsv[y][x])):
                temp.append(hsv[y][x][k])
            clrlst.append(temp)
        return clrlst


    def _import_yaml(self, confFile):
        '''
        Purpose:        The purpose of this function is to import the contents of the configuration file.
        Inputs:         string conf_file
        Outputs:        None
        Returns:        reference to configuration file
        Assumptions:    N/A
        '''
        assert (type(confFile) == str), "configuration file not passed as a string"
        with open(confFile, 'r') as file:
            doc = yaml.load(file)
            file.close()
        return doc


    def _get_file_size(self, pathname):
        '''
        Purpose:        The purpose of this function is to determine the size of the image
        Inputs:         string pathname
        Outputs:        None
        Returns:        int size of file in bytes
        Assumptions:    N/A
        '''
        return os.path.getsize(pathname)


    def _get_file_type(self, pathname):
        '''
        Purpose:        The purpose of this function is to determine the type of the image
        Inputs:         string pathname
        Outputs:        None
        Returns:        string file type (.ext)
        Assumptions:    N/A
        '''
        filename, fileExtension = os.path.splitext(pathname)
        return fileExtension


    def _set_types(self, tags, dateToString):
        '''
        Purpose:        The purpose of this function is to set the tag values to the correct
                        data type
        Inputs:         string pathname
                        bool dateToString toggles conversion of datetimeTags to strings
        Outputs:        None
        Returns:        string file type (.ext)
        Assumptions:    N/A
        '''
        for key, value in tags.iteritems():
            for entry in self.data["stringTags"]:
                if(key == entry):
                    tags[key] = str(value)
            for entry in self.data["datetimeTags"]:
                if(key == entry):
                    stringDate = str(value)
                    if dateToString is True:
                        tags[key] = stringDate
                    else:
                        tags[key] = datetime.strptime(stringDate, '%Y:%m:%d %H:%M:%S')
            for entry in self.data["intTags"]:
                if(key == entry):
                    strKey = str(value)
                    tags[key] = int(strKey)
        return tags
