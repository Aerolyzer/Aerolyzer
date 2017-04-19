'''
EXIF Data Retrieval File
Description: This file contains all functions for retrieving EXIF data from an image.
'''

import exifread
import yaml
from PIL import Image

class RtrvData(object):
    'Class containing all image restriction functions'

    def __init__(self):
        self.data = self._import_yaml("retrieve_image_data_conf.yaml")

    '''
    Purpose:        The purpose of this function is to retrieve the EXIF data from an
                    image.
    Inputs:         string path
    Outputs:        None
    Returns:        dictionary of EXIF data tags
    Assumptions:    The image's path has been provided
    '''
    def get_all_exif(self, path):
        img = open(path, 'rb')
        tags = exifread.process_file(img)
        return tags

    '''
    Purpose:        The purpose of this function is to retrieve the EXIF data from an
                    image.
    Inputs:         string path
    Outputs:        None
    Returns:        dictionary of EXIF data tags
    Assumptions:    The image's path has been provided
    '''
    def get_exif(self, path):
        tags = {};
        allTags = get_all_exif(path)
        for key, value in allTags.iteritems():
            if key in self.data['selectTags']:
                if type(value) == string:
                    tags[key.lower()] = value.lower()
                else:
                    tags[key.lower()] = value
            else:
        return tags

    '''
    Purpose:        The purpose of this function is to retrieve the RGB values from an
                    image.
    Inputs:         string path
    Outputs:        None
    Returns:        array of RGB values
    Assumptions:    The image's path has been provided
    '''
    def get_rgb(self, path):
        img = Image.open(path, 'r')
        pixels = list(img.getdata())
        return pixels

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
