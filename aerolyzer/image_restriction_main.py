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
def program(fxn, data, exifData, pathname):
    assert fxn.is_device(exifData['image model']), "The image must be a mobile image from a supported device"
    assert fxn.is_edited(exifData['image datetime'], exifData['exif datetimeoriginal']), "The image cannot be edited or filtered in any way"
    assert fxn.is_landscape(data.get_rgb(pathname)), "The image must be of a direct landscape with a sky and view"
    assert fxn.is_size(exifData['file size']), "The image must be no larger than 200kb"
    assert fxn.is_type(exifData['file type']), "The file type of the image must be .jpg or .png"
    assert fxn.is_res(exifData['exif exifimagewidth'], exifData['exif exifimagelength']), "The image must be in the resolution range 1X1-1000X1000"
    assert fxn.is_loc(exifData['gps gpslatitude'], exifData['gps gpslongitude']), "Location services must be enabled for the camera"

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

    #Retrieve exif data
    if(len(sys.argv) < 2):
        #use default image
        data    = Data("images/img2.jpg")
        exifData = data.get_exif("images/img2.jpg")
        program(fxn, data, exifData, "images/img2.jpg")
    elif(len(sys.argv) == 2):
        data    = Data(sys.argv[1])
        exifData = data.get_exif(sys.argv[1])
        program(fxn, data, exifData, sys.argv[1])
    elif(len(sys.argv) > 2):
        #error
        print "Please pass only 1 image to this program as an argument"

if __name__ == '__main__':
    main()
