'''
Image Restriction Function File
Description: This file contains all functions for the verifying image restrictions.
'''

import exifread
import re
import yaml

class imgRestFuncs(object):
    'Class containing all image restriction functions'

    def __init__(self):
        self.criteria = self._import_yaml("image_restriction_conf.yaml")
        assert (self.criteria['imgMaxSizeNumber'] == 200), "YAML import was not successful"

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
        if device in self.criteria['acceptedMobileDevices']):
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
        assert (type(created) == datetime), "Exif Image Width value not an integer"
        assert (type(modified) == datetime), "Exif Image Height value not an integer"
        
        if (created == modified):
            return True
        else:
            return False

    '''
    Purpose:        The purpose of this function is to determine whether or not the image
                    contains a direct landscape with sky and view.
    Inputs:         dict exifData, ?
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_landscape(self, exifData):
        pass
        #UNKNOWN METHOD

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
        #parse File Size parameter into a list of the numbers, spaces, and letters
        fileParameters = self._parse_file_size(fileSize)
        
        #check to make sure parsing was successful
        if(fileParameters == [] or len(fileParameters) != 3):
            return False
        else:
            if(fileParameters[2] == self.criteria['imgMaxSizeBytesShort'] or fileParameters[2] == self.criteria['imgMaxSizeBytesLong']):
                if(int(fileParameters[0]) <= self.criteria['imgMaxSizeNumber']):
                    return True
                else:
                    return False
            else:                
                for key, value in self.criteria['imgSizesLong'].iteritems():
                    if value == fileParameters[2]:
                        imgKey = key
                
                for key, value in self.criteria['imgSizesShort'].iteritems():
                    if value == fileParameters[2]:
                        imgKey = key
                
                for key, value in self.criteria['imgSizesShort'].iteritems():
                    if value == self.criteria['imgMaxSizeBytesShort']:
                        acceptImgKey = key

                if(imgKey < acceptImgKey):
                    return True

                elif(imgKey > acceptImgKey):
                    return False

                else:
                    return False

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

        if fileType in self.criteria['acceptedFileTypes']):
            return True
        else:
            return False

    '''
    Purpose:        The purpose of this function is to determine whether or not the image
                    exceeds the minimum resolution.
    Inputs:         int imageWidth, int imageHeight
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_res(self, imageWidth, imageHeight):
        assert (type(imageWidth) == int), "Exif Image Width value not an integer"
        assert (type(imageHeight) == int), "Exif Image Height value not an integer"

        if (imageWidth >= self.criteria['imgWidthMin'] and imageHeight >= self.criteria['imgHeightMin']):
            if (imageWidth <= self.criteria['imgWidthMax'] and imageHeight <= self.criteria['imgHeightMax']):
                return True
            else:
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
    Purpose:        The purpose of this function is to parse the file_size value into numbers
                    and letters.
    Inputs:         string file_size
    Outputs:        None
    Returns:        list file_parameters (digits, spaces, letters)
    Assumptions:    N/A
    '''
    def _parse(self, fileSize):
        assert (type(fileSize) == str), "fileSize not passed as a string"

        match = re.match(r"([0-9]+)(\s*)([a-z]+)$", fileSize, re.I)
        if match:
            fileParameters = match.groups()
        else:
            fileParameters = []
        return(fileParameters)

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
