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
    if not 'image model' in exifData:
        isVerified = {'meetsRest': False, 'error_message': "The image must be a mobile image from a supported device"}
        return isVerified
    if not fxn.is_device(exifData['image model']):
        isVerified = {'meetsRest': False, 'error_message': "The image must be a mobile image from a supported device"}
        return isVerified
    if not fxn.is_edited(exifData['image datetime'], exifData['exif datetimeoriginal']):
        isVerified = {'meetsRest': False, 'error_message': "The image cannot be edited or filtered in any way"}
        return isVerified
    if not fxn.is_landscape(data.get_rgb(pathname)):
        isVerified = {'meetsRest': False, 'error_message': "The image must be of a direct landscape with a sky and view"}
        return isVerified
    if not fxn.is_size(exifData['file size']):
        isVerified = {'meetsRest': False, 'error_message': "The image must be no larger than 400kb"}
        return isVerified
    if not fxn.is_type(exifData['file type']):
        isVerified = {'meetsRest': False, 'error_message': "The file type of the image must be .jpg or .png"}
        return isVerified
    if not fxn.is_res(exifData['exif exifimagewidth'], exifData['exif exifimagelength']):
        isVerified = {'meetsRest': False, 'error_message': "The image must be in the resolution range 1X1-1000X1000"}
        return isVerified
    if not 'gps gpslatitude' in exifData or not 'gps gpslongitude' in exifData:
        isVerified = {'meetsRest': False, 'error_message': "Location services must be enabled for the camera"}
        return isVerified
    locExifData = data.get_exif(pathname, False, False)
    exifData = data.get_exif(pathname, True, True)
    isVerified = {'meetsRest': True, 'exifData': exifData, 'locExifData': locExifData}
    return isVerified

'''
Purpose:        The purpose of this main function is to check all image restrictions
                for use in the Aerolyzer app.
Inputs:         string filename of image locally
Outputs:        None
Returns:        N/A
Assumptions:    N/A
'''
def check_image(filename):
    #instantiate classes
    fxn     = Fxn()
    #Retrieve exif data
    data    = Data(filename)
    exifData = data.get_exif(filename, True, False)
    isVerified = program(fxn, data, exifData, filename)
    return isVerified

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
        exifData = data.get_exif("images/img2.jpg", True, False)
        program(fxn, data, exifData, "images/img2.jpg")
    elif(len(sys.argv) == 2):
        data    = Data(sys.argv[1])
        exifData = data.get_exif(sys.argv[1], True, False)
        program(fxn, data, exifData, sys.argv[1])
    elif(len(sys.argv) > 2):
        #error
        print "Please pass only 1 image to this program as an argument"

if __name__ == '__main__':
    main()
