'''
EXIF Data Retrieval File
Description: This file contains all functions for retrieving EXIF data from an image.
'''

import exifread
import re
import yaml

class RtrvExif(object):
    'Class containing all image restriction functions'

    def __init__(self):
        self.criteria = self._import_yaml("image_restriction_conf.yaml")
        assert (self.criteria['imgMaxSizeNumber'] == 200), "YAML import was not successful"

    '''
    Purpose:        The purpose of this function is to retrieve the EXIF data from an
                    image.
    Inputs:         string path
    Outputs:        None
    Returns:        dictionary of EXIF data tags
    Assumptions:    The image's path has been provided
    '''
    def get_exif(self, path):
        assert (type(path) == str), "path not passed as a string"        
        img = open(path, 'rb')
        tags = exifread.process_file(img)
        return tags

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
