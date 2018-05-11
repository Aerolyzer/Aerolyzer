'''
Image Restriction Main File
Description: This file is called by the website when a photo is uploaded, and uses
information from image_restriction_functions and image_restrictions_conf to verify that
all image restrictions have been met.
'''

import sys

from image_restriction_functions import imgRestFuncs as Fxn
from retrieve_image_data import RtrvData as Data


def program(fxn, data, exifData, pathname):
    '''
    Purpose:        The purpose of this function is to assert each restriction check
    Inputs:         dict exifData, object functions
    Outputs:        restriction check results
    Returns:        isVerified
    Assumptions:    N/A
    '''
    if not 'image model' in exifData:
        isVerified = {'meetsRest': False, 'error_message': "The image must be a mobile image from a supported device"}
        return isVerified
    if not fxn.is_device(exifData['image model']):
        isVerified = {'meetsRest': False, 'error_message': "The image must be a mobile image from a supported device"}
        return isVerified
    if not fxn.is_edited(exifData['image datetime'], exifData['exif datetimeoriginal']):
        isVerified = {'meetsRest': False, 'error_message': "The image cannot be edited or filtered in any way"}
        return isVerified
    if not fxn.is_landscape(pathname):
        isVerified = {'meetsRest': False, 'error_message': "The image must be of a direct landscape with a sky and view"}
        return isVerified
    if not fxn.is_size(exifData['file size']):
        isVerified = {'meetsRest': False, 'error_message': "The image must be no larger than 4Mb"}
        return isVerified
    if not fxn.is_type(exifData['file type']):
        isVerified = {'meetsRest': False, 'error_message': "The file type of the image must be .jpg or .png"}
        return isVerified
    if not fxn.is_res(exifData['exif exifimagewidth'], exifData['exif exifimagelength']):
        isVerified = {'meetsRest': False, 'error_message': "The image must be in the resolution range 600X600-6000X6000"}
        return isVerified
    if not 'gps gpslatitude' in exifData or not 'gps gpslongitude' in exifData:
        isVerified = {'meetsRest': False, 'error_message': "Location services must be enabled for the camera"}
        return isVerified
    locExifData = data.get_exif(pathname, False, False)
    exifData = data.get_exif(pathname, True, True)
    isVerified = {'meetsRest': True, 'exifData': exifData, 'locExifData': locExifData}
    return isVerified


def check_image(filename,confPath="."):
    '''
    Purpose:        The purpose of this main function is to check all image restrictions
                    for use in the Aerolyzer app.
    Inputs:         string filename of image locally, optional string confPath
    Outputs:        None
    Returns:        isVerified
    Assumptions:    N/A
    '''
    #instantiate classes
    fxn     = Fxn(confPath)
    #Retrieve exif data
    data    = Data(confPath)
    exifData = data.get_exif(filename, True, False)
    isVerified = program(fxn, data, exifData, filename)
    return isVerified


def main():
    '''
    Purpose:        The purpose of this main function is to check all image restrictions and
                    produce the correct error message should one occur.
    Inputs:         string image (as sys.argv[1]), Config path(as sys.argv[2])
    Outputs:        None
    Returns:        N/A
    Assumptions:    N/A
    '''
    #instantiate classes
    

    #Retrieve exif data
    if(len(sys.argv) < 2):
        #error
        print "Please pass an image path as an argument with an optional config path"

    elif(len(sys.argv) == 2):
        check_image(sys.argv[1])

    elif(len(sys.argv) == 3):
        check_image(sys.argv[1],sys.argv[2])

    elif(len(sys.argv) > 3):
        #error
        print "Please pass only 1 image to this program and an optional config path as arguments"

if __name__ == '__main__':
    main()
