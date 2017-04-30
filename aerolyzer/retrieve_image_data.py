'''
Data Retrieval File
Description: This file contains all functions for retrieving data from an image.
'''

import os
import cv2
import yaml
import exifread
from datetime import datetime

class RtrvData(object):
    'Class containing all image restriction functions'

    def __init__(self, pathPassed):
        self.data = self._import_yaml("config/retrieve_image_data_conf.yaml")
        try:
            os.path.exists(pathPassed)
        except ImportError:
            pass

    '''
    Purpose:        The purpose of this function is to retrieve the EXIF data from an
                    image.
    Inputs:         string pathname
    Outputs:        None
    Returns:        dictionary of EXIF data tags
    Assumptions:    The image's path has been provided
    '''
    def _get_all_exif(self, pathname):
        img = open(pathname, 'rb')
        tags = exifread.process_file(img)
        return tags

    '''
    Purpose:        The purpose of this function is to retrieve the EXIF data from an
                    image.
    Inputs:         string pathname
    Outputs:        None
    Returns:        dictionary of EXIF data tags
    Assumptions:    The image's path has been provided
    '''
    def get_exif(self, pathname):
        tags = {};
        allTags = self._get_all_exif(pathname)
        for key, value in allTags.iteritems():
            for entry in self.data['selectTags']:
                if (key == entry):
                    tags[key.lower()] = value
        tags = self._set_types(tags)
        tags['file size'] = self._get_file_size(pathname)
        tags['file type'] = self._get_file_type(pathname).lower()
        return tags

    '''
    Purpose:        The purpose of this function is to retrieve the RGB values from an
                    image.
    Inputs:         string pathname
    Outputs:        None
    Returns:        tuple of lists of lists containing RGB values
    Assumptions:    The image's path has been provided
    '''
    def get_rgb(self, pathname):
        img = cv2.imread(pathname,1)
        return img

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
    
    '''
    Purpose:        The purpose of this function is to determine the size of the image
    Inputs:         string pathname
    Outputs:        None
    Returns:        int size of file in bytes
    Assumptions:    N/A
    '''
    def _get_file_size(self, pathname):
        return os.path.getsize(pathname)
    
    '''
    Purpose:        The purpose of this function is to determine the type of the image
    Inputs:         string pathname
    Outputs:        None
    Returns:        string file type (.ext)
    Assumptions:    N/A
    '''
    def _get_file_type(self, pathname):
        filename, fileExtension = os.path.splitext(pathname)
        return fileExtension
    
    '''
    Purpose:        The purpose of this function is to set the tag values to the correct
                    data type
    Inputs:         string pathname
    Outputs:        None
    Returns:        string file type (.ext)
    Assumptions:    N/A
    '''
    def _set_types(self, tags):
        for key, value in tags.iteritems():
            for entry in self.data['stringTags']:
                if(key == entry):
                    tags[key] = str(value)
            for entry in self.data['datetimeTags']:
                if(key == entry):
                    stringDate = str(value)
                    tags[key] = datetime.strptime(stringDate, '%Y:%m:%d %H:%M:%S')
            for entry in self.data['intTags']:
                if(key == entry):
                    strKey = str(value)
                    tags[key] = int(strKey)
        return tags
