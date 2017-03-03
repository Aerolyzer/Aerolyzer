'''
Aerolyzer
March 2, 2017
Image Restriction Function File
Description: This file contains all functions for the verifying image restrictions.
'''

'''
import libraries
'''
import re
import exifread

class imageRestrictionFunctions(object):
    'Class containing all image restriction functions'

    def __init__(self):
        pass

    '''
    Purpose:        The purpose of this function is to determine whether or not the device the
                    image was taken on is an accepted mobile device.
    Inputs:         dict exifData, list acceptedMobileDevices
    Outputs:        None
    Returns:        Boolean
    Assumptions:    N/A
    '''
    def accept_device(self, exifData, acceptedMobileDevices):
        #check to make sure the key-value pair exists in exifData to prevent errors
        if ('DEVICE' not in exifData.keys()):
            return False
        
        if any(exifData['DEVICE'].lower() in device for device in acceptedMobileDevices):
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
        #check to make sure the key-value pair exists in exifData to prevent errors
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
    def accept_size(self, exifData, imgMaxSizeNumber, imgMaxSizeBytesShort, imgMaxSizeBytesLong,
            imgSizesLong, imgSizesShort):
        #check to make sure the key-value pair exists in exifData to prevent errors
        if('File Size' not in exifData.keys()):
            return False
      
        #parse File Size parameter into a list of the numbers, spaces, and letters
        self.fileParameters = self.parse_file_size(exifData['File Size'])
        
        #check to make sure parsing was successful
        if(self.fileParameters == [] or len(self.fileParameters) != 3):
            return False
        else:
            #Case 1: File Size has same byte-type as the maximum value
            if(self.fileParameters[2].lower() == imgMaxSizeBytesShort or fileParameters[2].lower() == imgMaxSizeBytesLong):
                if(int(self.fileParameters[0]) <= imgMaxSize):
                    return True
                else:
                    return False
            else:                
                #Determine img byte-size key
                for self.key, self.value in imgSizesLong.iteritems():
                    if self.value == self.fileParameters[2].lower():
                        self.imgKey = self.key
                
                for self.key, self.value in imgSizesShort.iteritems():
                    if self.value == fileParameters[2].lower():
                        self.imgKey = self.key
                
                #Determine accepted img size byte-size key
                for self.key, self.value in imgSizesShort.iteritems():
                    if self.value == imgMaxSizeBytes:
                        self.acceptImgKey = self.key

                #Case 2: File Size byte-type is smaller
                if(self.imgKey < self.acceptImgKey):
                    return True

                #Case 3: File Size byte-type is larger
                elif(self.imgKey > self.acceptImgKey):
                    return False

                #Case 4: File Size byte-type unrecognized
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
    def accept_file_type(self, exifData, acceptedFileTypes):
        #check to make sure the key-value pair exists in exifData to prevent errors
        if('File Type' not in exifData.keys()):
            return False

        if any(exifData['File Type'].upper() in self.fileType for self.fileType in acceptedFileTypes):
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
    def accept_resolution(self, exifData, imgWidthMin, imgHeightMin, imgWidthMax, imgHeightMax):
        #check to make sure the key-value pair exists in exifData to prevent errors
        if('Exif Image Width' not in exifData.keys() or 'Exif Image Height'in exifData.keys()):
            return False
        
        if (exifData['Exif Image Width'] >= imgWidthMin and exifData['Exif Image Height'] >= imgHeightMin):
            if (exifData['Exif Image Width'] <= imgWidthMax and exifData['Exif Image Height'] <= imgHeightMax):
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
    def parse_file_size(self, fileSize):
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
    def error_message(self, boolean, imgRestrictionErrorText, error):
        if not boolean:
            return("Restriction Error: %s." % (imgRestrictionErrorText[error]))
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
    Purpose:        The purpose of this main function is to check all image restrictions and
                    produce the correct error message should one occur.
    Inputs:         None
    Outputs:        None
    Returns:        N/A
    Assumptions:    N/A
    '''
    def main():
        #Retrieve exif data
        exifData = get_exif(path)

        #Call each function and check for false return values
        error_message(accept_device(exifData, acceptedMobileDevices), imgRestrictionErrorText, 'accept_device')
        error_message(is_edited(exifData), imgRestrictionErrorText, 'is_edited')
        error_message(is_landscape(exifData), imgRestrictionErrorText, 'is_landscape')
        error_message(accept_size(exifData, imgMaxSize), imgRestrictionErrorText, 'accept_size')
        error_message(accept_file_type(exifData, acceptedFileTypes), imgRestrictionErrorText, 'accept_file_type')
        error_message(accept_resolution(exifData, imgWidthMin, imgHeightMin, imgWidthMax, imgHeighMax), imgRestrictionErrorText, 'accept_resolution')
        error_message(is_location_services(exifData), imgRestrictionErrorText, 'is_location_services')
