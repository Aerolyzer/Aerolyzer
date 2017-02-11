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
Image Criteria File
Purpose:        The purpose of this file is to keep all image criteria specifications located in
                one place, for simplicity's sake.
Inputs:         None
Outputs:        None
Returns:        None
Assumptions:    These values will be populated by a developer.
'''
accepted_file_types = ["JPEG", "JPG", "PNG"]
accepted_mobile_devices = ["i5", "i5s", "i6", "i6s", "i7"]
img_max_size = 200;
img_width_min = xxx;
img_height_min = xxx;

'''
Restriction:    The image must be from an accepted mobile device. 
Purpose:        The purpose of this function is to determine whether or not the device the
                image was taken on is an accepted mobile device.
Inputs:         EXIF data, list of accepted mobile devices
Outputs:        None
Returns:        True, False
Assumptions:    N/A
'''
def (**exif_data, accepted_mobile_devices):
    for device in range(len(accepted_mobile_devices)):
        if (exif_data[DEVICE] == accepted_mobile_devices[device]):
            return true
    return false

'''
Restriction:    The image cannot be edited or filtered in any way. 
Purpose:        The purpose of this function is to determine whether or not the image was
                altered from its original form. I.e. do the modification and creation dates coincide.
Inputs:         EXIF data
Outputs:        None
Returns:        True, False
Assumptions:    N/A
'''
def (**exif_data):
    if (exif_data[Create Date] == exif_data[Modify Date]):
        return true
    return false

'''
Restriction:    The image must be of a direct landscape with a sky and view.
Purpose:        The purpose of this function is to determine whether or not the image
                contains a direct landscape with sky and view.
Inputs:         EXIF data, ?
Outputs:        None
Returns:        True, False
Assumptions:    N/A
'''
def (**exif_data, ):
    #UNKNOWN METHOD

'''
Restriction:    The image must be no larger than 200kb.
Purpose:        The purpose of this function is to determine whether or not the size of
                the image is less than or equal to 200kb.
Inputs:         EXIF data, IMG_MAX_SIZE
Outputs:        None
Returns:        True, False
Assumptions:    N/A
'''
def (**exif_data, img_max_size):
    if (exif_data[File Size] <= img_max_size): #parsing may be necessary here "200 kB"
        return true
    return false

'''
Restriction:    The file type of the image must be .jpg or .png.
Purpose:        The purpose of this function  is to determine whether or not the image is
                an accepted file type.
Inputs:         EXIF data, list of accepted file types
Outputs:        None
Returns:        True, False
Assumptions:    N/A
'''
def (**exif_data, accepted_file_types):
    for file_type in range(len(accepted_file_types)):
        if (exif_data[File Type] == accepted_mobile_devices[file_type]):
            return true
    return false

'''
Restriction:    The image must exceed the minimum resolution. 
Purpose:        The purpose of this function is to determine whether or not the image
                exceeds the minimum resolution.
Inputs:         EXIF data, width and height of the image
Outputs:        None
Returns:        True, False
Assumptions:    N/A
'''
def (**exif_data, img_width_min, img_height_min):
    if (exif_data[Exif Image Width] >= img_width_min  && exif_data[Exif Image Height] >= img_height_min):
        return true
    return false

'''
Restriction:    Location services must be enabled for the camera
Purpose:        The purpose of this function is to determine whether or not the image was
                taken by a device with location services enabled for the camera.
Inputs:         EXIF data
Outputs:        None
Returns:        True, False
Assumptions:    N/A
'''
def (**exif_data):
    #may need to check that keys Latitude/Longitude exist before calling them below
    if (exif_data[Latitude] != null && exif_data[Longitude] != null):
        return true
    return false
