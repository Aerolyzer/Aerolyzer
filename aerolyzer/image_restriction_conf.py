'''
Aerolyzer
Feburary 28, 2017
Image Restriction Configuration File
Description: This configuration file stores information regarding image criteria that will
be evaluated in the image restrictions code.
'''

'''
import libraries
'''

'''
Image criteria values
'''

class imageRestrictionCriteria(object):
    'Class containing all image restriction criteria'
    
    acceptedFileTypes = ["JPEG", "JPG", "PNG"]
    acceptedMobileDevices = ["i5", "i5s", "i6", "i6s", "i7"]
    imgMaxSizeNumber = 200;
    imgMaxSizeBytesShort = "kb"
    imgMaxSizeBytesLong = "kilobytes"
    imgSizesLong =  {0: 'bytes',
                        1: 'kilobytes',
                        2: 'gigabytes',
                        3: 'megabytes',
                        4: 'terrabytes'}
    imgSizesShort =    {0: 'b',
                            1: 'kb',
                            2: 'gb',
                            3: 'mb',
                            4: 'tb'}
    imgWidthMin = 100;
    imgHeightMin = 100;
    imgWidthMax = 1000;
    imgHeightMax = 1000;
    imgRestrictionErrorText =  {'accept_device': 'The image must be a mobile image from a supported device',
                                'is_edited': 'The image cannot be edited or filtered in any way',
                                'is_landscape': 'The image must be of a direct landscape with a sky and view',
                                'accept_size': 'The image must be no larger than 200kb',
                                'accept_file_type': 'The file type of the image must be .jpg or .png',
                                'accept_resolution': 'The image must be in the resolution range 1X1-1000X1000',
                                'is_location_services': 'Location services must be enabled for the camera'}

    def __init__(self):
        pass


