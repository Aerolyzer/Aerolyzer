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

    '''
    Purpose:        The purpose of this function is to determine whether or not the device the
                    image was taken on is an accepted mobile device.
    Inputs:         dict exifData, list acceptedMobileDevices
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_accepted_device(self, exifData):
        if ('DEVICE' not in exifData.keys()):
            return False
        
        if any(exifData['DEVICE'].lower() in self.device for self.device in self.criteria['acceptedMobileDevices']):
            return True
        else:
            return False


    '''
    Purpose:        The purpose of this function is to determine whether or not the image was
                    altered from its original form. I.e. do the modification and creation dates coincide.
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_edited(self, exifData):
        if ('Create Date' not in exifData.keys() or 'Modify Date' not in exifData.keys()):
            return False
        
        if (exifData['Create Date'] == exifData['Modify Date']):
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
                    int imgMaxSizeBytesLong, dict imgSizesLong, dict imgSizesShort
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_accepted_size(self, exifData):
        if('File Size' not in exifData.keys()):
            return False
      
        #parse File Size parameter into a list of the numbers, spaces, and letters
        self.fileParameters = self._parse_file_size(exifData['File Size'])
        
        #check to make sure parsing was successful
        if(self.fileParameters == [] or len(self.fileParameters) != 3):
            return False
        else:
            if(self.fileParameters[2].lower() == self.criteria['imgMaxSizeBytesShort'] or fileParameters[2].lower() == self.criteria['imgMaxSizeBytesLong']):
                if(int(self.fileParameters[0]) <= self.criteria['imgMaxSizeNumber']):
                    return True
                else:
                    return False
            else:                
                for self.key, self.value in self.criteria['imgSizesLong'].iteritems():
                    if self.value == self.fileParameters[2].lower():
                        self.imgKey = self.key
                
                for self.key, self.value in self.criteria['imgSizesShort'].iteritems():
                    if self.value == fileParameters[2].lower():
                        self.imgKey = self.key
                
                for self.key, self.value in self.criteria['imgSizesShort'].iteritems():
                    if self.value == self.criteria['imgMaxSizeBytesShort']:
                        self.acceptImgKey = self.key

                if(self.imgKey < self.acceptImgKey):
                    return True

                elif(self.imgKey > self.acceptImgKey):
                    return False

                else:
                    return False

    '''
    Purpose:        The purpose of this function  is to determine whether or not the image is
                    an accepted file type.
    Inputs:         dict exifData, list acceptedFileTypes
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_accepted_type(self, exifData):
        if('File Type' not in exifData.keys()):
            return False

        if any(exifData['File Type'].upper() in self.fileType for self.fileType in self.criteria['acceptedFileTypes']):
            return True
        else:
            return False

    '''
    Purpose:        The purpose of this function is to determine whether or not the image
                    exceeds the minimum resolution.
    Inputs:         dict exifData, int imgWidthMin, int imgHeightMin
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_accepted_resolution(self, exifData):
        if('Exif Image Width' not in exifData.keys() or 'Exif Image Height'in exifData.keys()):
            return False
        
        if (exifData['Exif Image Width'] >= self.criteria['imgWidthMin'] and exifData['Exif Image Height'] >= self.criteria['imgHeightMin']):
            if (exifData['Exif Image Width'] <= self.criteria['imgWidthMax'] and exifData['Exif Image Height'] <= self.criteria['imgHeightMax']):
                return True
        else:
            return False

    '''
    Purpose:        The purpose of this function is to determine whether or not the image was
                    taken by a device with location services enabled for the camera.
    Inputs:         dict exifData
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_location_services(self, exifData):
        if('GPS Latitude' not in exifData.keys() or 'GPS Longitude' not in exifData.keys()):
            return False
        
        if (exifData['GPS Latitude'] != '' and exifData['GPS Longitude'] != ''):
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
    def _parse_file_size(self, fileSize):
        self.match = re.match(r"([0-9]+)(\s*)([a-z]+)$", fileSize, re.I)
        if self.match:
            self.fileParameters = match.groups()
        else:
            self.fileParameters = []
        return(self.fileParameters)


    '''
    Purpose:        The purpose of this function is to determine whether or not an image
                    restriction was passed, and print out the correct error statement accordingly.
    Inputs:         boolean bool, list imgRestrictionErrorText, key error
    Outputs:        None
    Returns:        Error message or blank message
    Assumptions:    N/A
    '''
    def err_msg(self, boolean, error):
        if not boolean:
            return("Restriction Error: %s." % (self.criteria['imgRestrictionErrorText'][error]))
        else:
            return('')

    '''
    Purpose:        The purpose of this main function is to check all image restrictions and
                    produce the correct error message should one occur.
    Inputs:         None
    Outputs:        None
    Returns:        N/A
    Assumptions:    N/A
    '''
    def get_exif(self, path):
        self.img = open(path, 'rb')
        self.tags = exifread.process_file(self.img)
        return self.tags

    '''
    Purpose:        The purpose of this function is to import the contents of the configuration file.
    Inputs:         string conf_file
    Outputs:        None
    Returns:        reference to configuration file
    Assumptions:    N/A
    '''
    def _import_yaml(self, conf_file):
        with open(conf_file, 'r') as self.file:
            self.doc = yaml.load(self.file)
            self.file.close()
        return self.doc