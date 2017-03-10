'''
Image Restriction Main File
Description: This file is called by the website when a photo is uploaded, and uses
information from image_restriction_functions and image_restrictions_conf to verify that
all image restrictions have been met.
'''

import sys

from image_restriction_functions import imgRestFuncs as Functions

'''
Purpose:        The purpose of this function is to assert each restriction check
Inputs:         dict exifData, object functions
Outputs:        restriction check results
Returns:        N/A
Assumptions:    N/A
'''
def program(exifData, functions):
    assert functions.is_accepted_device(exifData), "The image must be a mobile image from a supported device"
    assert functions.is_edited(exifData), "The image cannot be edited or filtered in any way"
    assert functions.is_landscape(exifData), "The image must be of a direct landscape with a sky and view"
    assert functions.is_accepted_size(exifData), "The image must be no larger than 200kb"
    assert functions.is_accepted_type(exifData), "The file type of the image must be .jpg or .png"
    assert functions.is_accepted_resolution(exifData), "The image must be in the resolution range 1X1-1000X1000"
    assert functions.is_location_services(exifData), "Location services must be enabled for the camera"

'''
Purpose:        The purpose of this function is to test restriction checks
Inputs:         dict exifData, object functions
Outputs:        restriction check results
Returns:        N/A
Assumptions:    N/A
'''
def test(functions):
    #Test function calls and assertions
    #functions.is_accepted_device("Hello World")
    #functions.is_accepted_size(200)
    tempExif = {'DEVICE': 'i5s',
                'File Size': '100 kb',
                'File Type': 'JPG',
                'Exif Image Width': 200,
                'Exif Image Height': 700}
    assert functions.is_accepted_device(tempExif), "The image must be a mobile image from a supported device"
    assert functions.is_accepted_size(tempExif), "The image must be no larger than 200kb"
    assert functions.is_accepted_type(tempExif), "The file type of the image must be .jpg or .png"
    assert functions.is_accepted_resolution(tempExif), "The image must be in the resolution range 100X100-1000X1000"

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
        test(functions)
    elif(len(sys.argv) == 2):
        exifData = functions.get_exif(sys.argv[1])
        test(functions)
    elif(len(sys.argv) > 2):
        #error
        print "Please pass only 1 image to this program as an argument"

if __name__ == '__main__':
    main()
