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
    Inputs:         dict exifData, list acceptedMobileDevices
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_accepted_device(self, exifData):
        assert (type(exifData) == dict), "exifData not passed as a dictionary"

        if ('DEVICE' not in exifData.keys()):
            return False   

        if any(exifData['DEVICE'].lower() in device for device in self.criteria['acceptedMobileDevices']):
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
        assert (type(exifData) == dict), "exifData not passed as a dictionary"

        if ('Create Date' not in exifData.keys() or 'Modify Date' not in exifData.keys()):
            return False

        assert (type(exifData['Create Date']) == datetime), "Exif Image Width value not an integer"
        assert (type(exifData['Modify Date']) == datetime), "Exif Image Height value not an integer"
        
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
        assert (type(exifData) == dict), "exifData not passed as a dictionary"

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
        assert (type(exifData) == dict), "exifData not passed as a dictionary"
        
        if('File Size' not in exifData.keys()):
            return False
      
        #parse File Size parameter into a list of the numbers, spaces, and letters
        fileParameters = self._parse_file_size(exifData['File Size'])
        
        #check to make sure parsing was successful
        if(fileParameters == [] or len(fileParameters) != 3):
            return False
        else:
            if(fileParameters[2].lower() == self.criteria['imgMaxSizeBytesShort'] or fileParameters[2].lower() == self.criteria['imgMaxSizeBytesLong']):
                if(int(fileParameters[0]) <= self.criteria['imgMaxSizeNumber']):
                    return True
                else:
                    return False
            else:                
                for key, value in self.criteria['imgSizesLong'].iteritems():
                    if value == fileParameters[2].lower():
                        imgKey = key
                
                for key, value in self.criteria['imgSizesShort'].iteritems():
                    if value == fileParameters[2].lower():
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
    Inputs:         dict exifData, list acceptedFileTypes
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def is_accepted_type(self, exifData):
        assert (type(exifData) == dict), "exifData not passed as a dictionary"

        if('File Type' not in exifData.keys()):
            return False

        assert (type(exifData['File Type']) == str), "File Type value not a string"

        if any(exifData['File Type'].upper() in fileType for fileType in self.criteria['acceptedFileTypes']):
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
        assert (type(exifData) == dict), "exifData not passed as a dictionary"

        if('Exif Image Width' not in exifData.keys() or 'Exif Image Height' not in exifData.keys()):
            return False

        assert (type(exifData['Exif Image Width']) == int), "Exif Image Width value not an integer"
        assert (type(exifData['Exif Image Height']) == int), "Exif Image Height value not an integer"

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
        assert (type(exifData) == dict), "exifData not passed as a dictionary"

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
        assert (type(fileSize) == str), "fileSize not passed as a string"

        match = re.match(r"([0-9]+)(\s*)([a-z]+)$", fileSize, re.I)
        if match:
            fileParameters = match.groups()
        else:
            fileParameters = []
        return(fileParameters)

    '''
    Purpose:        The purpose of this main function is to check all image restrictions and
                    produce the correct error message should one occur.
    Inputs:         None
    Outputs:        None
    Returns:        N/A
    Assumptions:    N/A
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
