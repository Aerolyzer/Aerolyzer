'''
Aerolyzer - Pseudocode
Feburary 10, 2017


Image Restrictions:

Throughout the upload process, images will be required to meet various
criteria beforee being accepted for aerosol content analysis. To accomplish this
requirement, a mulititude of functions will be created, each aimed at verifiying
that a certain restriction has been met. To ensure the simplicity of Aerolyzer's
initial development, as well as future adaptations, information regarding image criteria
will be stored in a single file to be referenced by the various restriction functions
outlined below.
'''

'''
Purpose:        The purpose of this file is to keep all image criteria specifications located in
                one place, for simplicity's sake.
Inputs:         None
Outputs:        None
Returns:        None
Assumptions:    These values will be populated by a developer.
'''
acceptedFileTypes = ["JPEG", "JPG", "PNG"]
acceptedMobileDevices = ["i5", "i5s", "i6", "i6s", "i7"]
imgMaxSize = 200;
imgWidthMin = xxx;
imgHeightMin = xxx;

'''
Purpose:        The purpose of this function is to determine whether or not the device the
                image was taken on is an accepted mobile device.
Inputs:         dict exifData, list acceptedMobileDevices
Outputs:        None
Returns:        Boolean
Assumptions:    N/A
'''
def accept_device(exifData, acceptedMobileDevices):
    #check to make sure the key-value pair exists in exifData to prevent errors
    if (exifData['DEVICE'] == null):
        return false
    
    if any(exifData['DEVICE'].lower() in device for device in acceptedMobileDevices):
        return true
    else:
        return false


'''
Purpose:        The purpose of this function is to determine whether or not the image was
                altered from its original form. I.e. do the modification and creation dates coincide.
Inputs:         dict exifData
Outputs:        None
Returns:        Boolean
Assumptions:    N/A
'''
def is_edited(exifData):
    #check to make sure the key-value pair exists in exifData to prevent errors
    if (exifData['Create Date'] == null or exifData['Modify Date'] == null):
        return false
    
    if (exifData['Create Date'] == exifData['Modify Date']):
        return true
    else:
        return false

'''
Purpose:        The purpose of this function is to determine whether or not the image
                contains a direct landscape with sky and view.
Inputs:         dict exifData, ?
Outputs:        None
Returns:        Boolean
Assumptions:    N/A
'''
def is_landscape(exifData, ):
    #UNKNOWN METHOD

'''
Purpose:        The purpose of this function is to determine whether or not the size of
                the image is less than or equal to 200kb.
Inputs:         dict exifData, int imgMaxSize
Outputs:        None
Returns:        Boolean
Assumptions:    N/A
'''
def accept_size(exifData, imgMaxSize):
    #check to make sure the key-value pair exists in exifData to prevent errors
    if(exifData['File Size'] == null):
        return false
    
    if (exifData['File Size'] <= imgMaxSize): #parsing may be necessary here "200 kB"
        return true
    else:
        return false

'''
Purpose:        The purpose of this function  is to determine whether or not the image is
                an accepted file type.
Inputs:         dict exifData, list acceptedFileTypes
Outputs:        None
Returns:        Boolean
Assumptions:    N/A
'''
def accept_file_type(exifData, acceptedFileTypes):
    #check to make sure the key-value pair exists in exifData to prevent errors
    if(exifData['File Type'] == null):
        return false

    if any(exifData['File Type'].upper() in fileType for fileType in acceptedFileTypes):
        return true
    else:
        return false

'''
Purpose:        The purpose of this function is to determine whether or not the image
                exceeds the minimum resolution.
Inputs:         dict exifData, int imgWidthMin, int imgHeightMin
Outputs:        None
Returns:        Boolean
Assumptions:    N/A
'''
def accept_resolution(exifData, imgWidthMin, imgHeightMin):
    #check to make sure the key-value pair exists in exifData to prevent errors
    if(exifData['Exif Image Width'] == null or exifData['Exif Image Height'] == null):
        return false
    
    if (exifData['Exif Image Width'] >= imgWidthMin  && exifData['Exif Image Height'] >= imgHeightMin):
        return true
    else:
        return false

'''
Purpose:        The purpose of this function is to determine whether or not the image was
                taken by a device with location services enabled for the camera.
Inputs:         dict exifData
Outputs:        None
Returns:        Boolean
Assumptions:    N/A
'''
def is_location_services(exifData):
    if(exifData['GPS Latitude'] == null or exifData['GPS Latitude'] == null):
        return false
    else:
        return true
