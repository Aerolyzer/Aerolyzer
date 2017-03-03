'''
Aerolyzer
March 2, 2017
Image Restriction Main File
Description: This file is called by the website when a photo is uploaded, and uses
information from image_restriction_functions and image_restrictions_conf to verify that
all image restrictions have been met.
'''

'''
import libraries
'''
import sys

'''
import references
'''
from image_restriction_conf import imageRestrictionCriteria as Criteria
from image_restriction_functions import imageRestrictionFunctions as Functions
    
    
'''
Purpose:        The purpose of this main function is to check all image restrictions and
                produce the correct error message should one occur.
Inputs:         string image (as sys.argv[1])
Outputs:        None
Returns:        N/A
Assumptions:    N/A
'''
def main():
    #instantiate classes
    functions = Functions()
    criteria = Criteria()

    #Retrieve exif data
    exifData = functions.get_exif(sys.argv[1])

    #Call each function and check for false return values
    print functions.error_message(functions.accept_device(exifData, criteria.acceptedMobileDevices),
            criteria.imgRestrictionErrorText, 'accept_device')
    print functions.error_message(functions.is_edited(exifData), criteria.imgRestrictionErrorText, 'is_edited')
    print functions.error_message(functions.is_landscape(exifData), criteria.imgRestrictionErrorText, 'is_landscape')
    print functions.error_message(functions.accept_size(exifData, criteria.imgMaxSizeNumber,
        criteria.imgMaxSizeBytesShort, criteria.imgMaxSizeBytesLong,
        criteria.imgSizesLong, criteria.imgSizesShort), criteria.imgRestrictionErrorText, 'accept_size')
    print functions.error_message(functions.accept_file_type(exifData, criteria.acceptedFileTypes), criteria.imgRestrictionErrorText, 'accept_file_type')
    print functions.error_message(functions.accept_resolution(exifData, criteria.imgWidthMin,
        criteria.imgHeightMin, criteria.imgWidthMax, criteria.imgHeightMax), criteria.imgRestrictionErrorText, 'accept_resolution')
    print functions.error_message(functions.is_location_services(exifData), criteria.imgRestrictionErrorText, 'is_location_services')


if __name__ == '__main__':
    main()
