'''
Image Restriction Main File
Description: This file is called by the website when a photo is uploaded, and uses
information from image_restriction_functions and image_restrictions_conf to verify that
all image restrictions have been met.
'''

import sys

from image_restriction_functions import imgRestFuncs as Functions

'''
Purpose:        The purpose of this function is to call each restriction check and print out the results
Inputs:         dict exifData
Outputs:        restriction check results
Returns:        N/A
Assumptions:    N/A
'''
def program(exifData, functions):
    #Call each function and check for false return values
    print functions.err_msg(functions.is_accepted_device(exifData), 'is_accepted_device')
    print functions.err_msg(functions.is_edited(exifData), 'is_edited')
    print functions.err_msg(functions.is_landscape(exifData), 'is_landscape')
    print functions.err_msg(functions.is_accepted_size(exifData), 'is_accepted_size')
    print functions.err_msg(functions.is_accepted_type(exifData), 'is_accepted_type')
    print functions.err_msg(functions.is_accepted_resolution(exifData), 'is_accepted_resolution')
    print functions.err_msg(functions.is_location_services(exifData), 'is_location_services')

 
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

    #Retrieve exif data
    if(len(sys.argv) < 2):
        #use default image
        exifData = functions.get_exif("images/img1.jpg")
        program(exifData, functions)
    elif(len(sys.argv) == 2):
        exifData = functions.get_exif(sys.argv[1])
        program(exifData, functions)
    elif(len(sys.argv) > 2):
        #error
        print "Please pass only 1 image to this program as an argument"

if __name__ == '__main__':
    main()
