'''
Image Restriction Main File
Description: This file is called by the website when a photo is uploaded, and uses
information from image_restriction_functions and image_restrictions_conf to verify that
all image restrictions have been met.
'''

import sys

from image_restriction_functions import imgRestFuncs as Fxn
from retrieve_image_data import RtrvData as Data

'''
Purpose:        The purpose of this function is to assert each restriction check
Inputs:         dict exifData, object functions
Outputs:        restriction check results
Returns:        N/A
Assumptions:    N/A
'''
def program(exifData, fxn):
    assert fxn.is_device(exifData), "The image must be a mobile image from a supported device"
    assert fxn.is_edited(exifData), "The image cannot be edited or filtered in any way"
    assert fxn.is_landscape(exifData), "The image must be of a direct landscape with a sky and view"
    assert fxn.is_size(exifData), "The image must be no larger than 200kb"
    assert fxn.is_type(exifData), "The file type of the image must be .jpg or .png"
    assert fxn.is_res(exifData), "The image must be in the resolution range 1X1-1000X1000"
    assert fxn.is_loc(exifData), "Location services must be enabled for the camera"

'''
Purpose:        The purpose of this function is to test restriction checks
Inputs:         dict exifData, object functions
Outputs:        restriction check results
Returns:        N/A
Assumptions:    N/A
'''
def test(fxn):
    #Test function calls and assertions
    #functions.is_accepted_device("Hello World")
    #functions.is_accepted_size(200)
    tempExif = {'DEVICE': 'i5s',
                'File Size': '100 kb',
                'File Type': 'JPG',
                'Exif Image Width': 200,
                'Exif Image Height': 700}
    assert fxn.is_device(tempExif), "The image must be a mobile image from a supported device"
    assert fxn.is_size(tempExif), "The image must be no larger than 200kb"
    assert fxn.is_type(tempExif), "The file type of the image must be .jpg or .png"
    assert fxn.is_res(tempExif), "The image must be in the resolution range 100X100-1000X1000"


'''
Purpose:        The purpose of this function is to test is_landscape function
Inputs:         fxn reference, rgb list of lists
Outputs:        None
Returns:        Boolean
Assumptions:    N/A
'''
def test_rgb(fxn, rgb):
    if fxn.is_landscape(rgb):
        return True
    else:
        return False 


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
    fxn     = Fxn()
    data    = Data()

    #Retrieve exif data
    if(len(sys.argv) < 2):
        #use default image
        exifData = data.get_exif("images/img2.jpg")
        rgb = data.get_rgb("images/img2.jpg")
        print test_rgb(fxn, rgb)
    elif(len(sys.argv) == 2):
        exifData = data.get_exif(sys.argv[1])
        rgb = data.get_rgb(sys.argv[1])
        print test_rgb(fxn, rgb)
    elif(len(sys.argv) > 2):
        #error
        print "Please pass only 1 image to this program as an argument"

if __name__ == '__main__':
    main()
